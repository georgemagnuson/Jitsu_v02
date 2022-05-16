#!/usr/bin/env python3
"""
Author : georgemagnuson@gmail.com
Date   : 2021-07-19
Purpose: tweepy wrapper using twitter API v2
"""

import argparse
import tweepy
from configparser import ConfigParser

# from icecream import ic
import rich
from datetime import datetime


def config(filename="database.ini", section="twitter"):
    parser = ConfigParser()
    parser.read(filename)
    auth = {}
    if parser.has_section(section):
        for param in parser[section].keys():
            auth[param] = parser.get(section, param, raw=True)
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )
    # rich.inspect(auth)
    return auth


def create_connection():
    """Connect to the twitter server"""
    auth = None
    # read connection parameters
    params = config()
    # connect to the twitter server
    auth = tweepy.OAuthHandler(params["api_key"], params["api_secret_key"])
    auth.set_access_token(params["access_token"], params["access_token_secret"])
    # auth = tweepy.Client( bearer_token=params["bearer_token"], consumer_key=params["api_key"], consumer_secret=params["api_secret_key"], access_token=params["access_token"], access_token_secret=params["access_token_secret"],)

    return auth


def send_a_DM(recipient_id="18240468", message="test DM"):
    dt = datetime.now()
    ts = (
        str(dt.year)[-2:]
        + ("0" + str(dt.month))[-2:]
        + ("0" + str(dt.day))[-2:]
        + "."
        + ("0" + str(dt.hour))[-2:]
        + ("0" + str(dt.minute))[-2:]
    )

    message = message.strip()[-67:] + " @" + ts

    auth = create_connection()
    api = tweepy.API(auth)

    api.send_direct_message(recipient_id=recipient_id, text=message)
    return


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Jitsu's twitter account sends a DM to gm4g2001",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-m",
        "--message",
        help="Direct Message",
        metavar="message",
        type=str,
        default="test DM",
    )

    parser.add_argument(
        "-i",
        "--id",
        help="recipient's id",
        metavar="id",
        type=str,
        default="18240468",
    )

    return parser.parse_args()


# --------------------------------------------------
# def get_user_info(api, id_arg):
#     user = api.get_user(user_id=id_arg)
#     rich.inspect(user)
#     return


def main():
    args = get_args()
    message_arg = args.message.strip()
    id_arg = args.id.strip()

    send_a_DM(id_arg, message_arg)


# --------------------------------------------------
if __name__ == "__main__":
    main()
