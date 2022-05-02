#!/usr/bin/env python3
"""
Author : georgemagnuson@gmail.com
Date   : 2021-09-29
Purpose: create a gmail dataclass
            that reads from gmail and writes to postgresql database
Returns:
"""
import base64
import os
import pickle
from configparser import ConfigParser
from dataclasses import dataclass
from datetime import datetime
from email import message_from_bytes, policy

# GMail API
# pip install --upgrade google-api-python-client google-auth-httplib2
# google-auth-oauthlib
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from rich.console import Console
from rich.progress import Progress

import pg8000

import message_v01


@dataclass
class GMailMessage:
    message_id: str
    gmail_service: str
    message_labels: list
    message_date: datetime
    message_from: str
    message_to: str
    message_subject: str
    message_raw: str
    message_has_attachment: bool = False
    deleted_row: bool = False

    # attachment_filename: str = None
    # attachment_raw: str = None

    def __init__(self, service, message_id):
        self.message_id = message_id
        self.gmail_service = service
        msg_full = (
            self.gmail_service.users()
            .messages()
            .get(userId="me", id=self.message_id, format="full")
            .execute()
        )
        msg_raw = (
            self.gmail_service.users()
            .messages()
            .get(userId="me", id=self.message_id, format="raw")
            .execute()
        )
        self.message_labels = msg_full["labelIds"]
        self.message_snippet = msg_full["snippet"]
        self.message_raw = msg_raw["raw"]
        email_obj = self.email_obj_from_raw_mail()
        datex = str(email_obj.get("Date"))
        self.message_date = datetime.strptime(
            datex, "%a, %d %b %Y %H:%M:%S %z")
        self.message_from = email_obj.get("From")
        self.message_to = email_obj.get("To")
        self.message_subject = email_obj.get("Subject")
        # value = self.email_obj_from_raw_mail().get(field)
        payload = email_obj.get_payload()
        if email_obj.is_multipart():
            for multipart in payload:
                if multipart.get_filename():
                    if "pdf" or "csv" in multipart.get_filename():
                        self.message_has_attachment = True
        #                 self.attachment_filename = multipart.get_filename()
        #                 self.attachment_raw = multipart.get_payload()
        return

    def save_message_to_postgresql(self):
        console = Console()
        if message_v01.select_first_message(self.message_id):
            console.log(f"[bright_yellow]WARNING: message id [white]{self.message_id}[/white] already exists.")
        else:
            message_v01.create_message(self.message_id, self.message_date, self.message_from, self.message_to, self.message_subject, self.message_has_attachment, self.message_raw)

        # console.log('adding SupplierMail/InvoicesProcessed label')
        # SupplierMail/InvoicesProcessed
        # self.message_label_add("Label_6569528190372695776")
        # console.log('removing SupplierMail/InvoicesNew label')
        # SupplierMail/InvoicesNew
        # self.message_label_remove("Label_6976860208836301729")
        # except (Exception, pg8000.DatabaseError) as error:
        #     console.log(f"[bold red]ERROR:{error}[/bold red]")
        # logger.error("error: {error_message}", error_message=error)
        # sql_console.rule("[bold red]ERROR")
        # sql_console.print(error)
        # finally:
        #     if sql_connection is not None:
        #         sql_connection.close()
                # console.log("Database connection closed.")
        return

    def get_message_full(self):
        """gets one specific message, full format, as given by message_id_arg"""
        msg_full = (
            self.gmail_service.users()
            .messages()
            .get(userId="me", id=self.message_id, format="full")
            .execute()
        )
        return msg_full

    def get_message_raw(self):
        """gets one specific message, raw format, as given by message_id_arg"""
        msg_raw = (
            self.gmail_service.users()
            .messages()
            .get(userId="me", id=self.message_id, format="raw")
            .execute()
        )
        return msg_raw

    def decode_base64url_utf8(self, raw):
        """decode raw message, base64url and utf-8"""
        decoded_bytes = base64.urlsafe_b64decode(raw)
        return str(decoded_bytes, "utf-8")

    # deal with individual message label: list, add or remove
    def message_labels_list(self):
        """return a list of message's labels"""
        self.message_labels = self.get_message_full()["labelIds"]
        return

    def message_label_add(self, label):
        """add a given label to a message"""
        console = Console()
        # available_labels = get_labels_list(service)
        # ic(available_labels)
        # current_labels = message_labels_list(service, message_id)
        if label in self.message_labels:
            # if label in current_labels:
            console.log(
                f"[bright_yellow]WARNING:\n label [white]{label}[/white] already exists for message."
            )
        else:
            mail_raw = (
                self.gmail_service.users()
                .messages()
                .modify(userId="me", id=self.message_id, body={"addLabelIds": label})
                .execute()
            )
            self.message_labels_list()
        # ic(current_labels)
        # else:
        #     print("[red]ERROR: message_label_add()")
        #     print(
        #         f"[red] label [white]{label}[/white] being added to message is not a part of available/usable labels"
        #     )
        return

    def message_label_remove(self, label):
        """remove label from message list of labels"""
        console = Console()
        # current_labels = self,message_labels_list(service, message_id)
        if label in self.message_labels:
            mail_raw = (
                self.gmail_service.users()
                .messages()
                .modify(userId="me", id=self.message_id, body={"removeLabelIds": label})
                .execute()
            )
            self.message_labels_list()
        else:
            console.log(
                f"[bright_yellow]WARNING: message_label_remove('{label}')")
            console.log(
                f"[bright_yellow] label [white]{label}[/white] is not currently a message label",
            )
        return

    # deals with extracting information from messages turning them into email
    # first
    def email_obj_from_raw_mail(self):
        """return email object from raw_mail"""
        decoded_msg_urlsafe = base64.urlsafe_b64decode(self.message_raw)
        return message_from_bytes(decoded_msg_urlsafe, policy=policy.default)

    def message_extract_attachments(self):
        """extracts pdf attachments from message"""
        email_obj = self.email_obj_from_raw_mail()
        # inspect(email_obj, all=True)
        # payload = email_obj.get_payload()
        # if email_obj.is_multipart():
        #     for multipart in payload:
        #         # inspect(multipart)
        #         # inspect(multipart.get_filename())
        #         # inspect(multipart.get_payload())
        #         if multipart.get_filename():
        #             if "pdf" or "csv" in multipart.get_filename():
        #                 filename = multipart.get_filename()
        #                 self.attachment_filename = filename[0]
        #                 attachment_raw = multipart.get_payload()
        #                 self.attachment_raw = attachment_raw[0]
        return

    def message_extract_field(self, field_name) -> str:
        """Extracts field from message"""
        if field_name == "raw":
            msg = self.get_message_raw()
        else:
            msg = self.get_message_full()
        return msg[field_name]

    def message_extract_fields(self) -> dict:
        """Extract given fields from message"""
        data = {"self": self.message_id}
        msg_raw = self.get_message_raw()
        msg_full = self.get_message_full()
        # inspect(email_obj_from_raw_mail(msg_raw['raw']).keys(), help=True)
        # for key, value in email_obj_from_raw_mail(msg_raw['raw']).items():
        #     print(f"KEY: [blue]{key}[/blue]\tVALUE: {value}")

        fields = [
            "Date",
            "From",
            "To",
            "Subject",
        ]
        # table = Table(title="FIELDS")
        # table.add_column("key", justify="left")
        # table.add_column("value")
        for field in fields:
            value = self.email_obj_from_raw_mail().get(field)
            # table.add_row(field, value)
            data[field] = value
            # table.add_row('snippet', msg_full["snippet"])
        data["raw"] = msg_raw["raw"]
        data["snippet"] = msg_full["snippet"]

        # data["attachment"] = self.message_extract_attachments()
        # TODO: add attachments as text body (coca-cola)
        # console = Console()
        # console.print(table)
        return data


@dataclass
class MailList:
    list_config_init_filename: str
    list_config_init_gmail_section: str
    list_config_init_db_section: str
    list_config_init_gmail: dict
    list_service: str
    pickle_path: str
    credentials_path: str
    scopes: str
    our_email: str
    folder_labels: list
    messages: list

    def __init__(self, filename="database.ini", section="gmail"):
        self.list_config_init_filename = filename
        self.list_config_init_gmail_section = section

        """config parser that reads settings"""
        parser = ConfigParser()
        parser.read(self.list_config_init_filename)

        self.list_config_init_gmail = {}
        if parser.has_section(self.list_config_init_gmail_section):
            params = parser.items(self.list_config_init_gmail_section)
            for param in params:
                if param[0] == "pickle_path":
                    self.pickle_path = param[1]
                elif param[0] == "credentials_path":
                    self.credentials_path = param[1]
                elif param[0] == "scopes":
                    self.scopes = param[1]
                elif param[0] == "our_email":
                    self.our_email = param[1]
                else:
                    self.list_config_init_gmail[param[0]] = param[1]
        else:
            raise Exception(
                f"Section {0} not found in the {1} file".format(
                    self.list_config_init_gmail_section, self.list_config_init_filename
                )
            )
        self.gmail_authenticate()
        return

    def gmail_authenticate(self):
        """authenticates token and credentials for gmail access"""
        creds = None
        # the file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time
        # ic(os.path.curdir)
        # ic(gmail['pickle_path'])
        # ic(os.path.exists(gmail['pickle_path']))
        if os.path.exists(self.pickle_path):
            with open(self.pickle_path, "rb") as token:
                creds = pickle.load(token)
        # if there are no (valid) credentials available, let the user log
        # in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.scopes
                )
                creds = flow.run_local_server(port=0)
            # save the credentials for the next run
            with open(self.pickle_path, "wb") as token:
                pickle.dump(creds, token)
        self.list_service = build("gmail", "v1", credentials=creds)
        return

    def get_labels_list(self):
        """get a list of folders"""
        # GET https://gmail.googleapis.com/gmail/v1/users/{userId}/labels
        self.folder_labels = (
            self.list_service.users().labels().list(userId="me").execute()
        )
        # result is initially a dict but below returns a list of labels
        return

    def perform_query_on_messages(self, query):
        """search in gmail form matches to query"""
        self.messages = []
        console = Console()
        console.log(f"performing query {query}")
        with console.status(
            "[bold green]Loading messages...", spinner="point"
        ) as status:
            result = (
                self.list_service.users()
                .messages()
                .list(userId="me", q=query)
                .execute()
            )
            if "messages" in result:
                # progress.console.print('Extending messages')
                self.messages.extend(result["messages"])
            while "nextPageToken" in result:
                # if there are more than one page of information keep getting them and
                # extend to messages
                # progress.console.print('getting nextPage of messages')
                page_token = result["nextPageToken"]
                result = (
                    self.list_service.users()
                    .messages()
                    .list(userId="me", q=query, pageToken=page_token)
                    .execute()
                )
                if "messages" in result:
                    console.log(f"extending messages {page_token}")
                    self.messages.extend(result["messages"])
        return

    def get_folder_messages(self, label_name):
        """returns all the messages in a given label/folder"""
        folder = "label:" + label_name
        self.perform_query_on_messages(folder)
        return

    def get_folder_messages_count(self, label):
        """return the number of messages in a given label/folder"""
        count = len(self.get_folder_messages(label))
        return count


def main():
    return


if __name__ == "__main__":
    main()

"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ id                             ┃ name                             ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ CHAT                           │ CHAT                             │
│ SENT                           │ SENT                             │
│ INBOX                          │ INBOX                            │
│ IMPORTANT                      │ IMPORTANT                        │
│ TRASH                          │ TRASH                            │
│ DRAFT                          │ DRAFT                            │
│ SPAM                           │ SPAM                             │
│ CATEGORY_FORUMS                │ CATEGORY_FORUMS                  │
│ CATEGORY_UPDATES               │ CATEGORY_UPDATES                 │
│ CATEGORY_PERSONAL              │ CATEGORY_PERSONAL                │
│ CATEGORY_PROMOTIONS            │ CATEGORY_PROMOTIONS              │
│ CATEGORY_SOCIAL                │ CATEGORY_SOCIAL                  │
│ STARRED                        │ STARRED                          │
│ UNREAD                         │ UNREAD                           │
│ Label_1                        │ Notes                            │
│ Label_9010196355161323194      │ mobi2go                          │
│ Label_221259640496078649       │ mobi2go/pickup                   │
│ Label_2562076789420739411      │ mobi2go/delivery                 │
│ Label_6910987098210624268      │ SupplierMail                     │
│ Label_6976860208836301729      │ SupplierMail/InvoicesNew         │
│ Label_6569528190372695776      │ SupplierMail/InvoicesProcessed   │
│ Label_2637890009347508683      │ SupplierMail/InvoicesUnprocessed │
│ Label_2921878595464026878      │ SupplierMail/Orders              │
│ Label_4332402040286630553      │ SupplierMail/PriceLists          │
│ Label_5381457617507387453      │ zz_Others                        │
│ Label_6804368613627176446      │ SupplierMail/Statement           │
└────────────────────────────────┴──────────────────────────────────┘
"""
