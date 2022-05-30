#!/usr/bin/env python3
"""
Author : Me <me@foo.com>
Date   : today
Purpose: Rock the Casbah
"""

import argparse
import logging
from logging.handlers import RotatingFileHandler

from rich import print
from rich.console import Console
from rich.logging import RichHandler

# console = Console()
# --------------------------------------------------


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Rock the Casbah",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("positional", metavar="str", help="A positional argument")

    parser.add_argument(
        "-a",
        "--arg",
        help="A named string argument",
        metavar="str",
        type=str,
        default="",
    )

    parser.add_argument(
        "-i",
        "--int",
        help="A named integer argument",
        metavar="int",
        type=int,
        default=0,
    )

    parser.add_argument(
        "-f",
        "--file",
        help="A readable file",
        metavar="FILE",
        type=argparse.FileType("r"),
        default=None,
    )

    parser.add_argument("-o", "--on", help="A boolean flag", action="store_true")

    parser.add_argument(
        "-l",
        "--logfile",
        help="Location of log file",
        metavar="FILE",
        type=argparse.FileType("a"),
        default=None,
    )

    parser.add_argument("-v", "--verbose", action="count", default=0)

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    str_arg = args.arg
    int_arg = args.int
    file_arg = args.file
    flag_arg = args.on
    logfile_arg = args.logfile
    verbose_arg = args.verbose
    pos_arg = args.positional

    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(verbose_arg, len(levels) - 1)]  # cap to last level index

    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                console=Console(file=logfile_arg),
                rich_tracebacks=True,
                tracebacks_show_locals=True,
                markup=True,
            ),
        ],
    )

    log = logging.getLogger(__name__)

    if logfile_arg:
        file_log = logging.getLogger("rotate file")
        file_handler = logging.handlers.RotatingFileHandler(
            filename=logfile_arg.name, mode="a", maxBytes=5000000, backupCount=1
        )
        file_log.addHandler(file_handler)

    # log.info("Hello, World!")
    # log.info(f'str_arg     = "{str_arg}"')
    # log.info(f'int_arg     = "{int_arg}"')
    # log.info('file_arg     = "{}"'.format(file_arg.name if file_arg else ""))
    # log.info(f'flag_arg    = "{flag_arg}"')
    # log.info('logfile_arg  = "{}"'.format(logfile_arg.name if logfile_arg else ""))
    # log.info(f'verbose_arg = "{verbose_arg}"')
    # log.info(f'positional  = "{pos_arg}"')
    # log.info(f'level       = "{level}"')
    #
    # # logging tests
    # log.debug("debug message")
    # log.info("info message")
    # log.warning("warning message")
    # log.error("error message")
    # log.critical("critical message")
    #
    # try:
    #     print(1 / 0)
    # except Exception:
    #     log.exception("unable print!")


# --------------------------------------------------
if __name__ == "__main__":
    main()
