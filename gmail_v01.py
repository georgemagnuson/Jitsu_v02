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
    messages = gmail.get_unread_inbox()
    rich.inspect(messages)
    # Starred messages
    # messages = gmail.get_starred_messages()

    # ...and many more easy to use functions can be found in gmail.py!

    # Print them out!
    for message in messages:
        rich.inspect(message)
        print("To: " + message.recipient)
        print("From: " + message.sender)
        print("Subject: " + message.subject)
        print("Date: " + message.date)
        print("Preview: " + message.snippet)

        print("Message Body: " + message.plain)  # or message.html

# --------------------------------------------------
if __name__ == '__main__':
    main()
