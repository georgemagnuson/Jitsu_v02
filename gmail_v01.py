#!/usr/bin/env python3
"""
Author : George Magnuson <georgemagnuson@gmail.com>
Date   : 2022 05 03
Purpose: try out jeremyephron/simplegmail
"""

import argparse
from simplegmail import Gmail
import rich


# --------------------------------------------------
# from simplegmail.simplegmail.label import Label


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

    gmail = Gmail()

    # Unread messages in your inbox
    # messages = gmail.get_unread_inbox()
    # id = 'Label_6976860208836301729'                                         │
    # name = 'SupplierMail/InvoicesNew'

    # Unread messages in inbox with label "SupplierMail/InvoicesNew"
    labels = gmail.list_labels()
    invoicesNew_label = list(filter(lambda x: x.name == 'SupplierMail/InvoicesNew', labels))[0]

    messages = gmail.get_unread_inbox(labels=[invoicesNew_label])
    for message in messages:
        rich.inspect(message)

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
