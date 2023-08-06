"""Main browser logic."""

import curses
import curses.ascii
import curses.textpad
import logging
import os
import subprocess
import tempfile
from importlib import import_module
from math import inf
from pathlib import Path
from typing import Optional, Tuple

from bebop.bookmarks import (
    get_bookmarks_path,
    get_bookmarks_document,
    save_bookmark,
)
from bebop.colors import A_ITALIC, ColorPair, init_colors
from bebop.command_line import CommandLine
from bebop.external import open_external_program
from bebop.fs import get_capsule_prefs_path, get_identities_list_path
from bebop.help import get_help
from bebop.history import History
from bebop.identity import load_identities
from bebop.links import Links
from bebop.metalines import LineType, RENDER_MODES
from bebop.mime import MimeType
from bebop.mouse import ButtonState
from bebop.navigation import (
    NO_NETLOC_SCHEMES,
    get_parent_url,
    get_root_url,
    join_url,
    parse_url,
    unparse_url,
)
from bebop.page import Page, get_render_options
from bebop.page_pad import PagePad
from bebop.preferences import load_capsule_prefs, save_capsule_prefs
from bebop.welcome import WELCOME_PAGE


class Browser:
    """Manage the events, inputs and rendering.

    Attributes:
    - config: config dict passed to the browser.
    - stash: certificate stash passed to the browser.
    - screen: curses stdscr.
    - dim: current screen dimensions.
    - page_pad: curses pad containing the current page view.
    - status_line: curses window used to report current status.
    - command_line: a CommandLine object for the user to interact with.
    - running: the browser will continue running while this is true.
    - status_data: 3-uple of status text, color pair and attributes of the
        status line, used to reset status after an error.
    - history: an History object.
    - cache: a dict containing cached pages.
    - special_pages: a dict containing page names used with "bebop" scheme;
        values are dicts as well: the "open" key maps to a callable to use when
        the page is accessed, and the optional "source" key maps to callable
        returning the page source path.
    - last_download: tuple of MimeType (may be None) and path, or None.
    - identities: identities map.
    - search_res_lines: list of lines containing results of the last search.
    """

    SEARCH_NEXT = 0
    SEARCH_PREVIOUS = 1

    def __init__(self, config, cert_stash):
        self.config = config
        self.stash = cert_stash
        self.screen = None
        self.dim = (0, 0)
        self.page_pad = None
        self.status_line = None
        self.command_line = None
        self.running = True
        self.status_data = ("", 0, 0)
        self.history = History(self.config["history_limit"])
        self.cache = {}
        self.special_pages = self.setup_special_pages()
        self.last_download: Optional[Tuple[Optional[MimeType], Path]] = None
        self.identities = {}
        self.search_res_lines = []
        self.plugins = []
        self._current_url = ""

    @property
    def h(self):
        return self.dim[0]

    @property
    def w(self):
        return self.dim[1]

    @property
    def current_url(self) -> str:
        """Return the current URL."""
        return self._current_url

    @current_url.setter
    def current_url(self, url: str):
        """Set the current URL and show it in the status line."""
        self._current_url = url
        self.set_status(url)

    @property
    def current_scheme(self):
        """Return the scheme of the current URL."""
        return parse_url(self._current_url)["scheme"] or ""

    @property
    def current_page(self) -> Optional[Page]:
        return self.page_pad.current_page

    def setup_special_pages(self):
        """Return a dict with the special pages functions."""
        return {
            "welcome": { "open": self.open_welcome_page },
            "help": { "open": self.open_help },
            "history": { "open": self.open_history },
            "bookmarks": {
                "open": self.open_bookmarks,
                "source": lambda: str(get_bookmarks_path())
            },
        }

    def run(self, *args, **kwargs):
        """Use curses' wrapper around _run."""
        os.environ.setdefault("ESCDELAY", "25")
        logging.info("Cursing…")
        curses.wrapper(self._run, *args, **kwargs)

    def _run(self, stdscr, start_url=None):
        """Start displaying content and handling events."""
        # Setup Curses.
        self.screen = stdscr
        self.screen.clear()
        self.screen.refresh()
        mousemask = curses.mousemask(curses.ALL_MOUSE_EVENTS)
        if mousemask == 0:
            logging.error("Could not enable mouse support.")
        curses.curs_set(0)
        init_colors()

        # Setup windows and pads.
        self.dim = self.screen.getmaxyx()
        self.page_pad = PagePad(self.h - 2)
        self.status_line = self.screen.subwin(
            *self.line_dim,
            *self.status_line_pos,
        )
        command_line_window = self.screen.subwin(
            *self.line_dim,
            *self.command_line_pos,
        )
        self.command_line = CommandLine(
            command_line_window,
            self.config["command_editor"]
        )

        # Load user data files, record which failed to load to warn the user.
        failed_to_load = []
        identities = load_identities(get_identities_list_path())
        if identities is None:
            failed_to_load.append("identities")
        else:
            self.identities = identities
        capsule_prefs = load_capsule_prefs(get_capsule_prefs_path())
        if capsule_prefs is None:
            failed_to_load.append("capsule preferences")
        else:
            self.capsule_prefs = capsule_prefs

        # Load user data files that may not exist (no warning).
        if self.config["persistent_history"]:
            if not self.history.load():
                logging.warning("Could not load history file.")

        # Load plugins.
        self.load_plugins()

        # If there has been any issue to load user files, show them instead of
        # automatically moving forward. Else either open the URL requested or
        # show the home page.
        if failed_to_load:
            error_msg = (
                f"Failed to open some local data: {', '.join(failed_to_load)}. "
                "These may be replaced if you continue."
            )
            self.set_status_error(error_msg)
        elif start_url:
            self.open_url(start_url)
        else:
            self.open_home()

        # Start listening for inputs.
        while self.running:
            try:
                self.handle_inputs()
            except KeyboardInterrupt:
                self.set_status("Cancelled.")

        if self.config["persistent_history"]:
            self.history.save()

    def handle_inputs(self):
        char = self.screen.getch()
        if char == ord("?"):
            self.open_help()
        elif char == ord(":"):
            self.quick_command("")
        elif char == ord("r"):
            self.reload_page()
        elif char == ord("h") or char == curses.KEY_LEFT:
            self.scroll_page_horizontally(-self.config["scroll_step"])
        elif char == ord("H"):
            self.scroll_whole_page_left()
        elif char == ord("j") or char == curses.KEY_DOWN:
            self.scroll_page_vertically(self.config["scroll_step"])
        elif char == ord("J") or char == curses.KEY_NPAGE:
            self.scroll_whole_page_down()
        elif char == ord("k") or char == curses.KEY_UP:
            self.scroll_page_vertically(-self.config["scroll_step"])
        elif char == ord("K") or char == curses.KEY_PPAGE:
            self.scroll_whole_page_up()
        elif char == ord("l") or char == curses.KEY_RIGHT:
            self.scroll_page_horizontally(self.config["scroll_step"])
        elif char == ord("L"):
            self.scroll_whole_page_right()
        elif char == ord("^"):
            self.scroll_page_horizontally(-inf)
        elif char == ord("g"):
            char = self.screen.getch()
            if char == ord("g"):
                self.scroll_page_vertically(-inf)
        elif char == ord("G"):
            self.scroll_page_vertically(inf)
        elif char == ord("o"):
            self.quick_command("open")
        elif char == ord("O"):
            self.quick_command(f"open {self.current_url}")
        elif char == ord("p"):
            self.go_back()
        elif char == ord("u"):
            self.go_to_parent_page()
        elif char == ord("U"):
            self.go_to_root_page()
        elif char == ord("b"):
            self.open_bookmarks()
        elif char == ord("B"):
            self.add_bookmark()
        elif char == ord("e"):
            self.edit_page()
        elif char == ord("y"):
            self.open_history()
        elif char == ord("m"):
            self.toggle_render_mode()
        elif char == ord("/"):
            self.search_in_page()
        elif char == ord("n"):
            self.move_to_search_result(Browser.SEARCH_NEXT)
        elif char == ord("N"):
            self.move_to_search_result(Browser.SEARCH_PREVIOUS)
        elif char == ord("!"):
            self.quick_command("exec")
        elif curses.ascii.isdigit(char):
            self.handle_digit_input(char)
        elif char == curses.KEY_MOUSE:
            try:
                self.handle_mouse(*curses.getmouse())
            except curses.error:
                logging.error("Failed to get mouse information.")
        elif char == curses.KEY_RESIZE:
            self.handle_resize()
        elif char == curses.ascii.ESC:  # Can be ESC or ALT char.
            self.screen.nodelay(True)
            char = self.screen.getch()
            self.screen.nodelay(False)
            if char == -1:
                self.reset_status()
            else:  # ALT keybinds.
                if char == ord("h"):
                    self.scroll_page_horizontally(-1)
                elif char == ord("j"):
                    self.scroll_page_vertically(1)
                elif char == ord("k"):
                    self.scroll_page_vertically(-1)
                elif char == ord("l"):
                    self.scroll_page_horizontally(1)
                elif char == ord("o"):
                    self.open_last_download()

    @property
    def page_pad_size(self):
        return self.h - 3, self.w - 1

    @property
    def status_line_pos(self):
        return self.h - 2, 0

    @property
    def command_line_pos(self):
        return self.h - 1, 0

    @property
    def line_dim(self):
        return 1, self.w

    def refresh_windows(self):
        """Refresh all windows and clear command line."""
        self.refresh_page()
        self.refresh_status_line()
        self.command_line.clear()

    def refresh_page(self):
        """Refresh the current page pad; it does not reload the page."""
        self.page_pad.refresh_content(*self.page_pad_size)

    def refresh_status_line(self):
        """Refresh status line contents."""
        text, pair, attributes = self.status_data
        logging.debug("Status: " + text)
        text = text[:self.w - 1]
        color = curses.color_pair(pair)
        self.status_line.addstr(0, 0, text, color | attributes)
        self.status_line.clrtoeol()
        self.status_line.refresh()

    def set_status(self, text):
        """Set a regular message in the status bar."""
        self.status_data = text, ColorPair.NORMAL, A_ITALIC
        self.refresh_status_line()

    def reset_status(self):
        """Reset status line, e.g. after a cancelled action."""
        self.set_status(self.current_url)

    def set_status_error(self, text):
        """Set an error message in the status bar."""
        self.status_data = text, ColorPair.ERROR, 0
        self.refresh_status_line()

    def quick_command(self, command):
        """Shortcut method to take user input with a prefixed command string."""
        prefix = command + " " if command else ""
        text = self.command_line.focus(CommandLine.CHAR_COMMAND, prefix=prefix)
        if not text:
            return
        self.process_command(text)

    def process_command(self, command_text: str):
        """Handle a client command."""
        words = command_text.split()
        num_words = len(words)
        if num_words == 0:
            return

        command = words[0]

        # Check for plugin registered commands first.
        for plugin in self.plugins:
            if command in map(lambda c: c.name, plugin.commands):
                plugin.use_command(self, command, command_text)
                return

        # Then built-in commands without args.
        if num_words == 1:
            if command == "help":
                self.open_help()
            elif command in ("q", "quit"):
                self.running = False
            elif command in ("h", "home"):
                self.open_home()
            elif command in ("i", "info"):
                self.show_page_info()
            else:
                self.set_status_error(f"Unknown command '{command}'.")
        # And commands with one or more args.
        else:
            if command in ("o", "open"):
                self.open_url(words[1])
            elif command == "exec":
                self.exec_external_command(words[1:])
            elif command == "forget-certificate":
                from bebop.browser.gemini import forget_certificate
                forget_certificate(self, words[1])
            elif command == "set-render-mode":
                self.set_render_mode(words[1])
            else:
                self.set_status_error(f"Unknown command '{command}'.")

    def get_user_text_input(self, status_text, char, prefix="", strip=False,
                            escape_to_none=False):
        """Get user input from the command-line."""
        self.set_status(status_text)
        result = self.command_line.focus(
            char,
            prefix=prefix,
            escape_to_none=escape_to_none
        )
        self.reset_status()
        if result is None:
            return None
        if strip:
            result = result.strip()
        return result

    def open_url(self, url, base_url=None, redirects=0, history=True,
                 use_cache=False):
        """Try to open an URL.

        This function assumes that the URL can be from an user and thus tries a
        few things to make it work.

        Arguments:
        - url: an URL string, may not be completely compliant.
        - base_url: an URL string to use as base in case `url` is relative.
        - redirections: number of redirections we did yet for the same request.
        - history: whether the URL should be pushed to history on success.
        - use_cache: whether we should look for an already cached document.
        """
        if redirects > 5:
            self.set_status_error(f"Too many redirections ({url}).")
            return

        # Take the current scheme as the default scheme to use if the URL does
        # not specify it. If it's the bebop scheme, discard it. If there is no
        # current scheme available, default to the gemini scheme.
        current_scheme = self.current_scheme
        if not current_scheme or current_scheme == "bebop":
            current_scheme = "gemini"
        parts = parse_url(url, default_scheme=current_scheme)

        # If there is no netloc part, try to join the URL.
        if (
            parts["netloc"] is None
            and parts["scheme"] == current_scheme
            and parts["scheme"] not in NO_NETLOC_SCHEMES
        ):
            url_is_usable = False
            # Join from either a given base URL, e.g. redirections or following
            # a relative link. If there is no such reference URL, try to guess
            # what the user meant to do.
            if base_url:
                parts = parse_url(join_url(base_url, url))
                url_is_usable = True
            elif parts["scheme"] and parts["path"]:
                guessed_url = parts["scheme"] + "://" + parts["path"]
                if self.prompt(f"Do you mean '{guessed_url}'?") == "y":
                    parts = parse_url(guessed_url)
                    url_is_usable = True
            # If nothing could be done, just give up.
            if not url_is_usable:
                self.set_status_error(f"Can't open '{url}'.")
                return

        # Replace URL passed as parameter by a sanitized one.
        url = unparse_url(parts)

        scheme = parts["scheme"]
        if scheme == "gemini":
            from bebop.browser.gemini import open_gemini_url
            success = open_gemini_url(
                self,
                url,
                redirects=redirects,
                use_cache=use_cache
            )
            if history and success:
                self.history.push(url)

        elif scheme.startswith("http"):
            from bebop.browser.web import open_web_url
            open_web_url(self, url)

        elif scheme == "file":
            from bebop.browser.file import open_file
            file_url = open_file(self, parts["path"])
            if history and file_url:
                self.history.push(file_url)

        elif scheme == "bebop":
            special_page = self.special_pages.get(parts["path"])
            if special_page:
                special_page["open"]()
            else:
                self.set_status_error("Unknown page.")

        else:
            from bebop.plugins import SchemePlugin
            plugins = (p for p in self.plugins if isinstance(p, SchemePlugin))
            plugin = next(filter(lambda p: p.scheme == scheme, plugins), None)
            if plugin:
                result_url = plugin.open_url(self, url)
                if history and result_url:
                    self.history.push(result_url)
            else:
                self.set_status_error(f"Protocol '{scheme}' not supported.")

    def load_page(self, page: Page):
        """Set this page as the current page and refresh appropriate windows."""
        old_pad_height = self.page_pad.dim[0]
        self.page_pad.show_page(page)
        if self.page_pad.dim[0] < old_pad_height:
            self.screen.clear()
            self.screen.refresh()
            self.refresh_windows()
        else:
            self.refresh_page()

    def handle_digit_input(self, init_char: int):
        """Focus command-line to select the link ID to follow."""
        if self.current_page is None:
            return
        links = self.current_page.links
        if links is None:
            return
        err, val = self.command_line.focus_for_link_navigation(init_char, links)
        if err == 0:
            self.open_link(links, val)  # type: ignore
        elif err == 2:
            self.set_status_error(val)

    def open_link(self, links: Links, link_id: int):
        """Open the link with this link ID."""
        if not link_id in links:
            self.set_status_error(f"Unknown link ID {link_id}.")
            return
        self.open_url(links[link_id], base_url=self.current_url)

    def handle_mouse(self, mouse_id: int, x: int, y: int, z: int, bstate: int):
        """Handle mouse events.

        Vertical scrolling is handled, and clicking on links.
        """
        if bstate & ButtonState.SCROLL_UP:
            self.scroll_page_vertically(-3)
        elif bstate & ButtonState.SCROLL_DOWN:
            self.scroll_page_vertically(3)
        elif bstate & ButtonState.LEFT_CLICKED:
            self.handle_mouse_click(x, y)

    def handle_mouse_click(self, x: int, y: int):
        """Handle a mouse click.

        If the click is on a link (appropriate line and columns), open it.
        """
        if not self.current_page:
            return
        px, py = self.page_pad.current_column, self.page_pad.current_line
        line_pos = y + py
        if line_pos >= len(self.current_page.metalines):
            return
        ltype, ltext, lextra = self.current_page.metalines[line_pos]
        if ltype != LineType.LINK:
            return
        # "url" key is contained only in the first line of the link if its text
        # is wrapped, so if the user did not click on the first line, rewind to
        # get the URL.
        while not lextra or "url" not in lextra:
            line_pos -= 1
            _, ltext, lextra = self.current_page.metalines[line_pos]
        url = lextra["url"]
        # The click is valid if it is on the link itself or the dimmed preview.
        col_pos = x + px
        if col_pos > len(ltext):
            ch = self.page_pad.pad.instr(line_pos, col_pos, 1)
            if ch == b' ':
                return
        self.open_url(url, base_url=self.current_url)

    def handle_resize(self):
        """Try to not make everything collapse on resizes."""
        # Refresh the whole screen before changing windows to avoid random
        # blank screens.
        self.screen.refresh()
        old_dim = self.dim
        self.dim = self.screen.getmaxyx()
        # Avoid work if the resizing does not impact us.
        if self.dim == old_dim:
            return
        # Resize windows to fit the new dimensions. Content pad will be updated
        # on its own at the end of the function.
        self.status_line.resize(*self.line_dim)
        self.command_line.window.resize(*self.line_dim)
        # Move the windows to their new position if that's still possible.
        if self.status_line_pos[0] >= 0:
            self.status_line.mvwin(*self.status_line_pos)
        if self.command_line_pos[0] >= 0:
            self.command_line.window.mvwin(*self.command_line_pos)
        # If the content pad does not fit its whole place, we have to clean the
        # gap between it and the status line. Refresh all screen.
        if self.page_pad.dim[0] < self.h - 2:
            self.screen.clear()
            self.screen.refresh()
        self.refresh_windows()

    def scroll_page_vertically(self, by_lines):
        """Scroll page vertically.

        If `by_lines` is an integer (positive or negative), scroll the page by
        this amount of lines. If `by_lines` is one of the floats inf and -inf,
        go to the end of file and beginning of file, respectively.
        """
        window_height = self.h - 2
        require_refresh = False
        if by_lines == inf:
            require_refresh = self.page_pad.go_to_end(window_height)
        elif by_lines == -inf:
            require_refresh = self.page_pad.go_to_beginning()
        else:
            require_refresh = self.page_pad.scroll_v(by_lines, window_height)
        if require_refresh:
            self.refresh_page()

    def scroll_whole_page_down(self):
        """Scroll down by a whole page."""
        self.scroll_page_vertically(self.page_pad_size[0])

    def scroll_whole_page_up(self):
        """Scroll up by a whole page."""
        self.scroll_page_vertically(-self.page_pad_size[0])

    def scroll_page_horizontally(self, by_columns):
        """Scroll page horizontally.

        If `by_lines` is an integer (positive or negative), scroll the page by
        this amount of columns. If `by_lines` is -inf, scroll back to the first
        column. Scrolling to the right-most column is not supported.
        """
        if by_columns == -inf:
            require_refresh = self.page_pad.go_to_first_column()
        else:
            require_refresh = self.page_pad.scroll_h(by_columns, self.w)
        if require_refresh:
            self.refresh_page()

    def scroll_whole_page_left(self):
        """Scroll left by a whole page."""
        self.scroll_page_horizontally(-self.page_pad_size[1])

    def scroll_whole_page_right(self):
        """Scroll right by a whole page."""
        self.scroll_page_horizontally(self.page_pad_size[1])

    def reload_page(self):
        """Reload the page, if one has been previously loaded."""
        if self.current_url:
            self.open_url(self.current_url, history=False, use_cache=False)

    def go_back(self):
        """Go back in history if possible."""
        if self.current_url.startswith("bebop:"):
            previous_url = self.history.get_previous(actual_previous=True)
        else:
            previous_url = self.history.get_previous()
        if previous_url:
            self.open_url(previous_url, history=False, use_cache=True)

    def go_to_parent_page(self):
        """Go to the parent URL if possible."""
        if self.current_url:
            self.open_url(get_parent_url(self.current_url))

    def go_to_root_page(self):
        """Go to the root URL if possible."""
        if self.current_url:
            self.open_url(get_root_url(self.current_url))

    def open_internal_page(self, name, gemtext):
        """Open some content corresponding to a "bebop:" internal URL."""
        page = Page.from_gemtext(gemtext, get_render_options(self.config))
        self.load_page(page)
        self.current_url = "bebop:" + name

    def open_bookmarks(self):
        """Open bookmarks."""
        content = get_bookmarks_document()
        if content is None:
            self.set_status_error("Failed to open bookmarks.")
            return
        self.open_internal_page("bookmarks", content)

    def add_bookmark(self):
        """Add the current URL as bookmark."""
        if not self.current_url:
            return
        current_title = self.current_page.title or ""
        title = self.get_user_text_input(
            "Bookmark title?",
            CommandLine.CHAR_TEXT,
            prefix=current_title,
            strip=True,
        )
        if title:
            save_bookmark(self.current_url, title)

    def edit_page(self):
        """Open a text editor to edit the page source.

        For external pages, the source is written in a temporary file, opened in
        its editor of choice and so it's up to the user to save it where she
        needs it, if needed. Internal pages, e.g. the bookmarks page, are loaded
        directly from their location on disk.
        """
        delete_source_after = False
        parts = parse_url(self.current_url)
        if parts["scheme"] == "bebop":
            page_name = parts["path"]
            special_pages_functions = self.special_pages.get(page_name)
            if not special_pages_functions:
                return
            get_source = special_pages_functions.get("source")
            source_filename = get_source() if get_source else None
        else:
            if not self.current_page:
                return
            source = self.current_page.source
            with tempfile.NamedTemporaryFile("wt", delete=False) as source_file:
                source_file.write(source)
                source_filename = source_file.name
            delete_source_after = True

        if not source_filename:
            return

        command = self.config["source_editor"] + [source_filename]
        success = open_external_program(command)
        if not success:
            self.set_status_error("Could not open editor.")

        if delete_source_after:
            os.unlink(source_filename)
        self.refresh_windows()

    def open_help(self):
        """Show the help page."""
        self.open_internal_page("help", get_help(self.config, self.plugins))

    def prompt(self, text: str, keys: str ="yn"):
        """Display the text and allow it to type one of the given keys."""
        choice = "/".join(keys)
        self.set_status(f"{text} [{choice}]")
        return self.command_line.prompt_key(keys)

    def open_history(self):
        """Show a generated history of visited pages."""
        self.open_internal_page("history", self.history.to_gemtext())

    def open_last_download(self):
        """Open the last downloaded file."""
        if not self.last_download:
            return
        mime_type, path = self.last_download
        main_type = mime_type.main_type if mime_type else ""
        command = self.config["external_commands"].get(main_type)
        if not command:
            command = self.config["external_command_default"]
        command = command + [str(path)]
        self.set_status(f"Running '{' '.join(command)}'...")
        try:
            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        except FileNotFoundError as exc:
            self.set_status_error(f"Failed to run command: {exc}")

    def open_home(self):
        """Open the home page."""
        self.open_url(self.config["home"])

    def open_welcome_page(self):
        """Open the default welcome page."""
        self.open_internal_page("welcome", WELCOME_PAGE)

    def show_page_info(self):
        """Show some page informations in the status bar."""
        page = self.current_page
        if not page:
            return
        mime = page.mime.short if page.mime else "unk. MIME"
        encoding = page.encoding or "unk. encoding"
        size = f"{len(page.source)} chars"
        lines = f"{len(page.metalines)} lines"
        info = f"{mime}  {encoding}  {size}  {lines}"
        self.set_status(info)

    def set_render_mode(self, mode):
        """Set the render mode for the current path or capsule."""
        if mode not in RENDER_MODES:
            valid_modes = ", ".join(RENDER_MODES)
            self.set_status_error("Valid render modes are: " + valid_modes)
            return
        url = self.get_user_text_input(
            f"Set '{mode}' render mode for which URL (includes children)?",
            CommandLine.CHAR_TEXT,
            prefix=self.current_url,
            strip=True
        )
        if not url:
            return
        prefs = self.capsule_prefs.get(url, {})
        prefs["render_mode"] = mode
        self.capsule_prefs[url] = prefs
        save_capsule_prefs(self.capsule_prefs, get_capsule_prefs_path())
        self.reload_page()

    def toggle_render_mode(self):
        """Switch to the next render mode for the current page."""
        page = self.current_page
        if not page or page.render_opts is None:
            return
        render_opts = page.render_opts
        current_mode = render_opts.mode
        if current_mode not in RENDER_MODES:
            next_mode = RENDER_MODES[0]
        else:
            cur_mod_index = RENDER_MODES.index(current_mode)
            next_mode = RENDER_MODES[(cur_mod_index + 1) % len(RENDER_MODES)]
        render_opts.mode = next_mode
        new_page = Page.from_gemtext(page.source, render_opts)
        self.load_page(new_page)
        self.set_status(f"Using render mode '{next_mode}'.")

    def search_in_page(self):
        """Search for words in the page."""
        if not self.current_page:
            return
        search = self.get_user_text_input("Search", CommandLine.CHAR_TEXT)
        if not search:
            return
        self.search_res_lines = []
        for index, (_, ltext, _) in enumerate(self.current_page.metalines):
            if search in ltext:
                self.search_res_lines.append(index)
        if self.search_res_lines:
            self.move_to_search_result(Browser.SEARCH_NEXT)
        else:
            self.set_status(f"'{search}' not found.")

    def move_to_search_result(self, prev_or_next: int):
        """Move to the next or previous search result."""
        current_line = self.page_pad.current_line
        next_line = None
        index = 1
        max_index = len(self.search_res_lines)
        if prev_or_next == Browser.SEARCH_NEXT:
            for line in self.search_res_lines:
                if line > current_line:
                    next_line = line
                    break
                index += 1
        elif prev_or_next == Browser.SEARCH_PREVIOUS:
            index = max_index
            for line in reversed(self.search_res_lines):
                if line < current_line:
                    next_line = line
                    break
                index -= 1
        if next_line is None:
            return

        self.set_status(f"Result {index}/{max_index}")
        max_line = self.page_pad.get_max_line(self.h)
        self.page_pad.current_line = min(next_line, max_line)
        self.refresh_windows()

    def load_plugins(self):
        """Load installed and configured plugins."""
        for plugin_name in self.config["enabled_plugins"]:
            module_name = f"bebop_{plugin_name}"

            try:
                module = import_module(module_name)
            except ImportError as exc:
                logging.error(f"Could not load module {module_name}: {exc}")
                continue

            try:
                self.plugins.append(module.plugin)  # type: ignore
            except AttributeError:
                logging.error(f"Module {module_name} does not export a plugin.")
                continue

            logging.info(f"Loaded plugin {plugin_name}.")

    def exec_external_command(self, command):
        pass
