#!/usr/bin/env python3
"""
Author : Me <me@foo.com>
Date   : today
Purpose: Rock the Casbah
"""

import argparse
import logging
from rich import print
from rich.console import Console
from rich.logging import RichHandler

console = Console()
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
    verbose_arg = args.verbose
    pos_arg = args.positional
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(verbose_arg, len(levels) - 1)]  # cap to last level index
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )

    print(f'str_arg = "{str_arg}"')
    print(f'int_arg = "{int_arg}"')
    print('file_arg = "{}"'.format(file_arg.name if file_arg else ""))
    print(f'flag_arg = "{flag_arg}"')
    print(f'verbose_arg = "{verbose_arg}"')
    print(f'positional = "{pos_arg}"')

    # logging tests
    logging.debug("debug message")
    logging.info("info message")
    logging.warning("warning message")
    logging.error("error message")
    logging.critical("critical message")


# --------------------------------------------------
if __name__ == "__main__":
    main()
