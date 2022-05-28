#!/usr/bin/env python3
"""
Author : George Magnuson <georgemagnuson@gmail.com>
Date   : 2022 05 14
Purpose: went back to jitsu_gmail
"""

import argparse
import os

import rich
from pydantic.types import UUID4
import logging
from rich import print
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from rich.logging import RichHandler

import twitter_v02
import jitsu_gmail.gmail_dataclass

# import jitsu_gmail.gmail_message
from model.message import (
    save_message_to_postgresql,
    select_all_messages_limit,
    create_db_and_tables,
)

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="get emails from google folder and save to postgresql database",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # parser.add_argument("positional", metavar="str", help="username")

    # parser.add_argument(
    #     "-p", "--password", help="password", metavar="str", type=str, default=""
    # )

    parser.add_argument(
        "-t", "--test", help="turn on non-destructive mode", action="store_true"
    )

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
    log = logging.getLogger("rich")
    # console.print(logging.getLevelName(0))
    # console.print(logging.getLevelName("DEBUG"))
    # console.print(logging.getLevelName(10))
    # console.print(logging.getLevelName(3))
    # log.setLevel(logging.DEBUG)
    # log.setLevel(logging.INFO)
    log.setLevel(logging.WARNING)
    # log.setLevel(logging.ERROR)
    # log.setLevel(logging.CRITICAL)
    args = get_args()
    # username = args.positional
    # password = args.password
    test_mode = args.test
    # print(f'username = "{username}"')
    # print(f'password = "{password}"')
    if test_mode:
        log.setLevel(logging.INFO)
        log.info("test mode - non-destructive on")
    # Unread messages in your inbox
    # messages = gmail.get_unread_inbox()
    # id = 'Label_6976860208836301729'
    # name = 'SupplierMail/InvoicesNew'

    # try:
    #     print(1 / 0)
    # except Exception:
    #     log.exception("unable print!")

    log.info("initializing gmail_messages mail list object")
    gmail_messages = jitsu_gmail.gmail_dataclass.MailList("database.ini", "gmail")

    # console.print(print_labelNames(gmail_messages.folder_labels))

    log.info(
        "collect messages from SupplierMail/InvoicesNew into gmail_messages mail list"
    )

    gmail_messages.get_folder_messages("SupplierMail/InvoicesNew")
    message_count = len(gmail_messages.messages)
    tweet = f"{os.path.basename(__file__)}: {message_count} new message"
    if message_count > 1:
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
                # progress.console.rule()
                progress.console.print(
                    f"processing message_id: [blue]{progress_note[0:100]}"
                )
                # progress.console.print(
                #     f"original labelIds    : [blue]{gmail_message.message_labelIds}"
                # )

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

                gmail_message.get_labelNames(gmail_messages.folder_labels)
                progress.console.print(
                    f"label names          : [bright_blue]{gmail_message.message_labelNames}"
                )

                progress.advance(task)

    log.info(f"{tweet}")
    if not test_mode:
        twitter_v02.send_a_DM(message=tweet)

    log.info("done.")


"""
    messages = gmail.get_unread_inbox(labels=[invoicesNew_label])
    if len(messages) > 0:
        tweet: str = f"gmail: {len(messages)} message"
        if len(messages) > 1:
            tweet = tweet + "s"
        twitter_v02.send_a_DM(message=tweet)
    print(
        f"[blue]{invoicesNew_label.name}[/blue] message count: [bold red]{len(messages)}[/bold red]"
    )
    for message in messages:
        # rich.inspect(message)
        console.rule()

        print(f"[bright_black]To        : [bright_white]{message.recipient}[/]")
        print(f"[bright_black]From      : [bright_white]{message.sender}[/]")
        print(f"[bright_black]Date      : [bright_white]{message.date}[/]")
        print(f"[bright_black]Subject   : [bright_white]{message.subject}[/]")
        print(f"[bright_black]Snippet   : [bright_white]{message.snippet}[/]")
        print(f"[bright_black]Attachment: [bright_white]{message.attachments}[/]")
        if message.attachments:
            for attachment in message.attachments:
                print(f"[white]\tFile Name: [bright_white]{attachment.filename}[/]")

    # labels = gmail.list_labels()
    # rich.inspect(labels)
    # for label in labels:
    #    rich.inspect(label)

"""
# --------------------------------------------------
if __name__ == "__main__":
    main()
