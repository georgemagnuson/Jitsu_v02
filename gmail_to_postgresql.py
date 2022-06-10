#!/usr/bin/env python3
"""
Author : George Magnuson <georgemagnuson@gmail.com>
Date   : 2022 05 14
Purpose: went back to jitsu_gmail
"""

import argparse
import os

import logging
from rich.progress import Progress
from rich.table import Table
from logging.handlers import RotatingFileHandler

# from rich import print
from rich.console import Console
from rich.logging import RichHandler

import twitter_v02
import jitsu_gmail.gmail_dataclass

from model.message import (
    save_message_to_postgresql,
    create_db_and_tables,
)


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="get emails from google folder and save to postgresql database",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-t", "--test", help="turn on non-destructive mode", action="store_true"
    )

    parser.add_argument(
        "-l",
        "--logfile",
        help="Location of log file",
        metavar="FILE",
        type=argparse.FileType("a"),
        # default=os.path.splitext(os.path.basename(__file__))[0] + ".log",
        default=None,
    )

    parser.add_argument("-v", "--verbose", action="count", default=0)

    return parser.parse_args()


def print_labelNames(folder_labels: dict):
    table = Table(title="GMail labels")
    table.add_column(
        "ID",
    )
    table.add_column(
        "Name",
    )
    for key in folder_labels.keys():
        table.add_row(key, folder_labels[key])
    return table


# --------------------------------------------------
def main():
    console = Console()
    args = get_args()
    test_mode = args.test
    logfile_arg = args.logfile
    # default=os.path.splitext(os.path.basename(__file__))[0] + ".log",
    verbose_arg = args.verbose
    if logfile_arg and verbose_arg == 0:
        verbose_arg = 1

    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(verbose_arg, len(levels) - 1)]  # cap to last level index

    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                rich_tracebacks=True,
                tracebacks_show_locals=True,
                markup=True,
            ),
        ],
    )

    console_file_handler = None
    file_handler = None

    if logfile_arg:
        file_handler = RotatingFileHandler(
            filename=logfile_arg.name,
            mode="a",
            maxBytes=5000000,
            backupCount=1,
        )
        console_file_handler = RichHandler(
            console=Console(file=logfile_arg),
            rich_tracebacks=True,
            tracebacks_show_locals=True,
            markup=True,
        )

    log = logging.getLogger(__name__)

    if verbose_arg > 0 and logfile_arg:
        log.addHandler(console_file_handler)

    if verbose_arg == 0 and logfile_arg:
        log.addHandler(file_handler)

    log.info("\n********************\n")

    if test_mode:
        log.info("test mode - non-destructive on")

    # Unread messages in your inbox
    # messages = gmail.get_unread_inbox()
    # id = 'Label_6976860208836301729'
    # name = 'SupplierMail/InvoicesNew'

    log.info("initializing gmail_messages mail list object")
    gmail_messages = jitsu_gmail.gmail_dataclass.MailList("database.ini", "gmail")

    log.info(
        "collect messages from SupplierMail/InvoicesNew into gmail_messages mail list"
    )
    gmail_messages.get_folder_messages("SupplierMail/InvoicesNew")
    message_count = len(gmail_messages.messages)
    log.info(f"message count: {message_count}")
    tweet = f"{os.path.basename(__file__)}: {message_count} new message"
    if message_count > 0:
        gmail_messages.get_labels_list()
        console.log("creating database and tables")
        create_db_and_tables()
        tweet = f"{os.path.basename(__file__)}: {message_count} new messages"
        with Progress() as progress:
            task = progress.add_task("Processing GMail", total=message_count)
            for message_id in gmail_messages.messages:
                progress.console.rule()
                gmail_message = jitsu_gmail.gmail_dataclass.GMailMessage(
                    gmail_messages.list_service, message_id["id"]
                )

                progress_note = (
                    gmail_message.message_id
                    + ": "
                    + gmail_message.message_date.strftime("%b %d %Y")
                    + " "
                    + gmail_message.message_subject
                    + " "
                    + gmail_message.message_from
                )
                progress.console.print(
                    f"processing message_id: [blue]{progress_note[0:100]}"
                )
                log.info(f"processing message_id: {progress_note[0:150]}")

                gmail_message.get_labelNames(gmail_messages.folder_labels)
                progress.console.print(
                    f"label names          : [bright_blue]{gmail_message.message_labelNames}"
                )

                progress.console.print(
                    f"[bright_black]saving message id    : [blue]{gmail_message.message_id} [bright_black]to postgresql"
                )
                if not test_mode:
                    save_message_to_postgresql(
                        gmail_message.message_id,
                        gmail_message.message_date,
                        gmail_message.message_from,
                        gmail_message.message_to,
                        gmail_message.message_subject,
                        gmail_message.message_has_attachment,
                        gmail_message.message_raw,
                    )
                    gmail_message.message_label_add("Label_6569528190372695776")
                    gmail_message.message_label_remove("Label_6976860208836301729")
                    log.info(f"processed {progress_note[0:100]}")

                gmail_message.get_labelNames(gmail_messages.folder_labels)
                progress.console.print(
                    f"label names          : [bright_blue]{gmail_message.message_labelNames}"
                )

                progress.advance(task)

    log.info(f"{tweet}")
    if not test_mode:
        twitter_v02.send_a_DM(message=tweet)

    log.info("done.")

    # try:
    #     print(1 / 0)
    # # except Exception:
    # except ArithmeticError:
    #     log.exception("unable print!")


# --------------------------------------------------
if __name__ == "__main__":
    main()
