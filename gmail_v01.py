#!/usr/bin/env python3
"""
Author : George Magnuson <georgemagnuson@gmail.com>
Date   : 2022 05 03
Purpose: try out jeremyephron/simplegmail
"""

import argparse
from simplegmail import Gmail
import rich
from rich import print
from rich.console import Console


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='try out jeremyephron/simplemail',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('positional',
                        metavar='str',
                        help='username')

    parser.add_argument('-p',
                        '--password',
                        help='password',
                        metavar='str',
                        type=str,
                        default='')

    return parser.parse_args()


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
    invoicesNew_label = list(filter(lambda x: x.name == 'SupplierMail/InvoicesNew', labels))[0]
    # rich.inspect(invoicesNew_label)

    messages = gmail.get_unread_inbox(labels=[invoicesNew_label])
    print(f'[blue]{invoicesNew_label.name}[/blue] message count: [bold red]{len(messages)}[/bold red]')
    for message in messages:
        # rich.inspect(message)
        console.rule()
        print('[grey]grey[/]')
        print('[white]white[/]')
        print('[bright white]bright white[/]')
        print('[silver]silver[/]')
        print('[blue]blue [/][bright blue]bright blue [/][salmon]salmon[/]')
        print(f'[maroon]maroon[/]')
        print(f'[orange]orange[/]')
        print(f'[green]green[/]')

        print(f'[white]To        : [bright_white]{message.recipient}[/]')
        print(f'[bright_black]From      : [bright_white]{message.sender}[/]')
        print(f'[white]Date      : [bright_white]{message.date}[/]')
        print(f'[white]Subject   : [bright_white]{message.subject}[/]')
        print(f'[white]Snippet   : [bright_white]{message.snippet}[/]')
        print(f'[white]Attachment: [bright_white]{message.attachments}[/]')
        if message.attachments:
            for attachment in message.attachments:
                print(f'[white]\tFile Name: [bright_white]{attachment.filename}[/]')
    # Starred messages
    # messages = gmail.get_starred_messages()

    # labels = gmail.list_labels()
    # rich.inspect(labels)
    # for label in labels:
    #    rich.inspect(label)

    # Print them out!
    # for message in messages:
    #     rich.inspect(message)
    #     print("To: " + message.recipient)
    #     print("From: " + message.sender)
    #     print("Subject: " + message.subject)
    #     print("Date: " + message.date)
    #     print("Preview: " + message.snippet)
    #
    #     print("Message Body: " + message.plain)  # or message.html


# --------------------------------------------------
if __name__ == '__main__':
    main()
