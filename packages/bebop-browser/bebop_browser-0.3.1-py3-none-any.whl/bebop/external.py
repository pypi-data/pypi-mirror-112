"""Call external commands."""

import curses
import logging
import re
import subprocess


def open_external_program(command):
    """Call command as a subprocess, suspending curses rendering.

    The caller has to refresh whatever windows it manages after calling this
    method or garbage may be left on the screen.

    Returns:
    True if no exception occured.
    """
    curses.nocbreak()
    curses.echo()
    curses.curs_set(1)
    result = True
    try:
        subprocess.run(command)
    except OSError as exc:
        logging.error(f"Failed to run '{command}': {exc}")
        result = False
    curses.mousemask(curses.ALL_MOUSE_EVENTS)
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    return result


def substitute_external_command(command, url, page):
    """Substitute "%" parts of the command with corresponding values.

    This uses standard Python template strings. Valid substitutions are:
    - $$ = $
    - $u = current url
    - $n (with n any positive number) = link url
    """
    pass
