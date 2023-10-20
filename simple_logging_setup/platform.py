import sys
import os

try:
    # syslog is only on unix based systems available
    import syslog  # NOQA: F401

    _SYSLOG_IS_AVAILABLE = True

except ImportError:
    _SYSLOG_IS_AVAILABLE = False


def terminal_supports_colors():
    if 'TERMINAL_SUPPORTS_COLORS' in os.environ:
        return True

    return (
        # check if stdout is a tty
        hasattr(sys.stdout, 'isatty') and
        sys.stdout.isatty()
    ) and (
        # Windows checks
        sys.platform != 'win32' or
        'ANSICON' in os.environ or

        # Windows Terminal supports VT codes
        'WT_SESSION' in os.environ or

        # Microsoft Visual Studio Code's built-in terminal supports colors
        os.environ.get('TERM_PROGRAM') == 'vscode'
    )


def colors_are_enabled():
    # https://no-color.org/

    return 'NO_COLOR' not in os.environ


def journald_is_running():
    return 'JOURNAL_STREAM' in os.environ and 'TERM' not in os.environ


def syslog_is_available():
    return _SYSLOG_IS_AVAILABLE
