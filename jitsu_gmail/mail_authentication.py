# from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
# other scopes:
#
#  scope = ["https://www.googleapis.com/auth/gmail.modify"]
# scopes = (["https://www.googleapis.com/auth/drive.metadata.readonly"],)
# scope=["https://mail.google.com/"]


def authenticate(
    token_json_path: str,
    credentials_json_path: str,
    scope: str,
):
    """Shows basic usage of the Gmail API."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_json_path):
        creds = Credentials.from_authorized_user_file(
            token_json_path, scopes=[f"{scope}"]
        )
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_json_path, scopes=[f"{scope}"]
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_json_path, "w") as token:
            token.write(creds.to_json())

    service = None

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)

        if not service:
            print("No service found.")
            return

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")

    return service
