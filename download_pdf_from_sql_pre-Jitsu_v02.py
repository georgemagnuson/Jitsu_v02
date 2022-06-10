#!/usr/bin/env python3
"""
Author : georgemagnuson@gmail.com
Date   : 2022-02-06
Purpose: just save a pdf from a given gmail message id
            previously saved to a postgresql database

Returns: extracted attachments in specified directory

sample/s:
        17c3840822dd3002 -> /tmp/attachments/Sales - Tax Invoice SI01972871.pdf
        170e057331aaa22c -> /tmp/attachments/108128395.pdf
        17c37f84d3e5421e -> /tmp/attachments/FreshoInvoice#F9422731.pdf
        17c2bf0860a17380 -> /tmp/attachments/Trents Invoice 198226444.pdf
        17ead8d28fa78610 -> /tmp/attachments/131214552.pdf (statement)
        17eabccd4118d612 -> /tmp/attachments/BidvestInvoices_20220131(5775).csv
        17e8aa9539854233 -> no attachments from Coca-cola -> save as text or html
        17ed89646495e2dc -> Tokyo Foods -> save multiple attachments (in folder?)
        1792f64990b7b8cb -> /tmp/attachments/W5685020210503112220.pdf

        "17c3840822dd3002 170e057331aaa22c 17c37f84d3e5421e 17c2bf0860a17380 17ead8d28fa78610 17eabccd4118d612 17e8aa9539854233 17ed89646495e2dc 1792f64990b7b8cb"
"""

import argparse
from loguru import logger
import pytest
from rich import inspect
from rich.console import Console
from rich.progress import Progress

import database


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="save pdf from message id to /tmp",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("positional", metavar="str", help="message id")

    return parser.parse_args()


# --------------------------------------------------
def main():
    console = Console()
    logger.add(
        "/tmp/download_pdf_from_sql.log",
        colorize=True,
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        rotation="1 week",
        backtrace=True,
        diagnose=True,
    )

    """Make a jazz noise here"""

    logger.info("starting main()")

    args = get_args()
    pos_arg = args.positional

    print(f'positional = "{pos_arg}"')

    dir_arg = "/tmp/attachments"

    for one_arg in pos_arg.split(" "):
        results = database.select_first_message(one_arg)

        if results:
            attachments = database.message_extract_attachments(
                one_arg, results.message_raw
            )
            if attachments:
                database.save_attachment_to_dir(
                    dir_arg=dir_arg, attachments=attachments
                )

    logger.info("--- e n d ---")


# --------------------------------------------------
if __name__ == "__main__":
    main()
