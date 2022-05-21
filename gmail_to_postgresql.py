#!/usr/bin/env python3
"""
Author : George Magnuson <georgemagnuson@gmail.com>
Date   : 2022 05 14
Purpose: went back to jitsu_gmail
"""

import argparse
import os

import rich
from rich import print
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

import twitter_v02
import jitsu_gmail.gmail_dataclass

# import jitsu_gmail.gmail_message
# import model.message


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="get emails from google folder and save to postgresql database",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("positional", metavar="str", help="username")

    parser.add_argument(
        "-p", "--password", help="password", metavar="str", type=str, default=""
    )

    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    # args = get_args()
    # username = args.positional
    # password = args.password
    # print(f'username = "{username}"')
    # print(f'password = "{password}"')

    # Unread messages in your inbox
    # messages = gmail.get_unread_inbox()
    # id = 'Label_6976860208836301729'
    # name = 'SupplierMail/InvoicesNew'

    console = Console()

    # console.log("creating database and tables")
    # model.message.create_db_and_tables()

    console.log("initializing gmail_messages mail list object")
    gmail_messages = jitsu_gmail.gmail_dataclass.MailList("database.ini", "gmail")

    gmail_messages.get_labels_list()
    table = Table(title="GMail labels")
    table.add_column(
        "ID",
    )
    table.add_column(
        "Name",
    )
    for key in gmail_messages.folder_labels.keys():
        table.add_row(key, gmail_messages.folder_labels[key])
    console.print(table)

    console.log(
        "collect messages from SupplierMail/InvoicesNew into gmail_messages mail list"
    )

    gmail_messages.get_folder_messages("SupplierMail/InvoicesNew")
    message_count = len(gmail_messages.messages)
    tweet = f"{os.path.basename(__file__)}: {message_count} new message"
    if message_count > 1:
        tweet = tweet + "s"
    console.log(
        f"{os.path.basename(__file__)}: there are [red]{message_count}[/red] new message/s."
    )
    # twitter_v02.send_a_DM(message=tweet)

    with Progress() as progress:
        task = progress.add_task("Processing GMail", total=message_count)
        for message in gmail_messages.messages:
            gmail_message = jitsu_gmail.gmail_dataclass.GMailMessage(
                gmail_messages.list_service, message["id"]
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
            progress.console.print(
                f"original labels      : [blue]{gmail_message.message_labels}"
            )
            label_names = []
            for label_id in gmail_message.message_labels:
                progress.console.print(gmail_messages.folder_labels[label_id])

            progress.console.print(f"label names : [bright_blue]{label_names}")

            # for label in gmail_message.message_labels:
            # progress.console.print(gmail_messages.folder_labels)

            # progress.console.print(
            #     f'saving message id    : [blue]{message["id"]} to postgresql'
            # )
            # message.save_message_to_postgresql()
            # progress.console.print(
            #     "[bright_black]adding SupplierMail/InvoicesProcessed label"
            # )
            # SupplierMail / InvoicesProcessed
            # gmail_message.message_label_add("Label_6569528190372695776")

            # progress.console.print(
            #     "[bright_black]removing SupplierMail/InvoicesNew label"
            # )
            # SupplierMail/InvoicesNew
            # progress.console.print(
            #     f"final labels         : [blue]{gmail_message.message_labels}"
            # )
            # gmail_message.message_label_remove("Label_6976860208836301729")

            progress.advance(task)

    console.log("done.")


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
