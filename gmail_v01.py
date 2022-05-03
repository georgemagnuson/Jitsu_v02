#!/usr/bin/env python3
"""
Author : George Magnuson <georgemagnuson@gmail.com>
Date   : 2022 05 03
Purpose: try out charlierguo/gmail
"""

import argparse
import gmail

# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='try out charlierguo/gmail',
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

    args = get_args()
    user_arg = args.positional
    password_arg = args.password

    print(f'user_arg = "{user_arg}"')
    print(f'password_arg = "{password_arg}"')

    # g = gmail.login(username, password)


# --------------------------------------------------
if __name__ == '__main__':
    main()
