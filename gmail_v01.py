#!/usr/bin/env python3
"""
Author : George Magnuson <georgemagnuson@gmail.com>
Date   : 2022 05 03
Purpose: try out jeremyephron/simplegmail
"""

import argparse

import rich
from rich import print
from rich.console import Console

import twitter_v02
from simplegmail import Gmail


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="try out jeremyephron/simplemail",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("positional", metavar="str", help="username")

    parser.add_argument(
        "-p", "--password", help="password", metavar="str", type=str, default=""
    )

    return parser.parse_args()


# def return_
#
#
#
# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    # args = get_args()
    # username = args.positional
    # password = args.password

    # print(f'username = "{username}"')
    # print(f'password = "{password}"')
    console = Console()
    gmail = Gmail()

    # Unread messages in your inbox
    # messages = gmail.get_unread_inbox()
    # id = 'Label_6976860208836301729'
    # name = 'SupplierMail/InvoicesNew'

    # Unread messages in inbox with label "SupplierMail/InvoicesNew"
    labels = gmail.list_labels()
    invoicesNew_label = list(
        filter(lambda x: x.name == "SupplierMail/InvoicesNew", labels)
    )[0]
    # rich.inspect(invoicesNew_label)

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


# --------------------------------------------------
if __name__ == "__main__":
    main()
