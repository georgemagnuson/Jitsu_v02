import base64
import os
import uuid
from configparser import ConfigParser
from datetime import date
from email import message_from_bytes, policy
from os.path import exists
from typing import List, Optional

import pydantic
from pydantic import UUID4
from rich.console import Console
from rich.progress import Progress
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

from model import base


# ---- fill parameters for postgresql access from .ini file
def config(filename="database.ini", section="postgresql"):
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


params = config()

PG_URL = "postgresql+pg8000://{}:{}@{}:{}/{}".format(
    params["user"],
    params["password"],
    params["host"],
    params["port"],
    params["database"],
)

# engine = create_engine(PG_URL, echo=True)
engine = create_engine(PG_URL, echo=False)


def create_db_and_tables():
    """run SQLModel to create database and table"""
    SQLModel.metadata.create_all(engine)


class Message(base.BaseWithUUID, table=True):
    """this holds the gmail_message SQL model class"""

    gmail_message_id: str
    message_date: date
    message_from: str
    message_to: str
    message_subject: str
    message_has_attachments: bool
    message_raw: Optional[str] = None
    message_processed: Optional[bool] = None
    message_status: Optional[str] = None


# ┌───────────────────────────────────────────┐
# │         MESSAGES related functions        │
# └───────────────────────────────────────────┘

# ┌───────────────────────────────────────────┐
# │   Individual MESSAGE related functions    │
# └───────────────────────────────────────────┘


def create_message(
    mail_message_id: str,
    mail_message_date: date,
    mail_message_from: str,
    mail_message_to: str,
    mail_message_subject: str,
    mail_message_has_attachments: bool,
    mail_message_raw: str,
):
    """extracted gmail info saved as postgresql message"""
    message_1 = Message(
        gmail_message_id=mail_message_id,
        message_date=mail_message_date,
        message_from=mail_message_from,
        message_to=mail_message_to,
        message_subject=mail_message_subject,
        message_has_attachments=mail_message_has_attachments,
        message_raw=mail_message_raw,
    )

    with Session(engine) as session:
        session.add(message_1)

        session.commit()

    return message_1


def save_message_to_postgresql(
    gmail_message_id,
    mail_message_date: date,
    mail_message_from: str,
    mail_message_to: str,
    mail_message_subject: str,
    mail_message_has_attachments: bool,
    mail_message_raw: str,
):
    console = Console()
    if select_first_message(gmail_message_id):
        console.log(
            f"[bright_yellow]WARNING: message id [white]{gmail_message_id}[/white] already exists in postgresql."
        )
    else:
        create_message(
            gmail_message_id,
            mail_message_date,
            mail_message_from,
            mail_message_to,
            mail_message_subject,
            mail_message_has_attachments,
            mail_message_raw,
        )

    # console.log("adding SupplierMail/InvoicesProcessed label")
    # SupplierMail/InvoicesProcessed
    # message.message_label_add("Label_6569528190372695776")
    # console.log("removing SupplierMail/InvoicesNew label")
    # SupplierMail/InvoicesNew
    # message.message_label_remove("Label_6976860208836301729")
    # except (Exception, pg8000.DatabaseError) as error:
    #     console.log(f"[bold red]ERROR:{error}[/bold red]")
    # console.log("error: {error_message}", error_message=error)
    # sql_console.rule("[bold red]ERROR")
    # sql_console.print(error)
    # finally:
    #     if sql_connection is not None:
    #         sql_connection.close()
    # console.log("Database connection closed.")
    return


def update_message_processed_status(message: Message, processed: bool, status: str):
    """update message status as being processed or not"""
    with Session(engine) as session:
        statement = select(Message).where(Message.id == message.id)
        results = session.exec(statement)
        new_message = results.one()
        # update the processed and status fields
        new_message.message_processed = processed
        new_message.message_status = status
        # commit changes to database
        session.add(new_message)
        session.commit()


def email_obj_from_raw_mail(raw_email):
    """return a fully formed email object from raw_mail"""
    decoded_msg_urlsafe = base64.urlsafe_b64decode(raw_email)
    return message_from_bytes(decoded_msg_urlsafe, policy=policy.default)


def message_extract_attachments(raw_email):
    """extracts all format attachments from message"""
    attachments = {}
    email_obj = email_obj_from_raw_mail(raw_email)
    payload = email_obj.get_payload()
    if email_obj.is_multipart():
        for multipart in payload:
            if multipart.get_filename():
                filename = multipart.get_filename()
                attachment_raw = multipart.get_payload()
                attachments.update({filename: attachment_raw})
    return attachments


def save_attachment_to_dir(dir_arg="/tmp/attachments", attachments=None):
    """Save attachments to directory"""
    # console = Console()
    try:
        # console.log(f"Creating directory: {dir_arg}")
        os.mkdir(dir_arg)
    except OSError as error:
        pass
        # console.log(f"[bright_yellow]Don't panic. Error: {error}")

    for key in attachments:
        filename = key
        attachment = attachments[key]
        filepath = os.path.join(dir_arg, filename)
        fp = open(filepath, "wb")
        fp.write(base64.b64decode(attachment))
        fp.close()
        # console.log(f'Filename: "{filepath}" written.')


def delete_attachment(filepath):
    """Delete temporary attachments after successful invoice2data"""
    console = Console()
    try:
        # console.log(f'Deleting {filepath}')
        os.remove(filepath)
    except OSError as error:
        console.log(f"[bright_yellow]OSError: {error}")


# ┌───────────────────────────────────────────┐
# │     Multiple MESSAGE related functions    │
# └───────────────────────────────────────────┘


def select_all_messages():
    """Read all messages"""
    with Session(engine) as session:
        statement = select(Message)
        results = session.exec(statement)
        return results


def select_all_messages_limit(limit: int):
    """Read messages with limit"""
    with Session(engine) as session:
        statement = select(Message).limit(limit)
        results = session.exec(statement)
        return results


def select_messages_with(sql: str, limit=0):
    """Read all messages with sql and limit"""
    console = Console()
    with Session(engine) as session:
        if limit == 0:
            statement = select(Message).where(text(sql))
        else:
            statement = select(Message).where(text(sql)).limit(limit)
        results = session.exec(statement)
        if results:
            for result in results:
                console.log(
                    f"Message {result.gmail_message_id} from {result.message_from}"
                )
        return results


def select_first_message(mail_message_id: str):
    """Read one message"""
    with Session(engine) as session_1:
        statement_1 = select(Message).where(Message.gmail_message_id == mail_message_id)
        result = session_1.exec(statement_1).first()
        return result


# def select_unprocessed_messages(sql="", qty=0):
#     """Read unprocessed messages"""
#     total_converted = 0
#     total_failed = 0
#     console = Console()
#     with Session(engine) as session:
#         if sql == "":
#             if qty == 0:
#                 statement = (
#                     select(Message, Invoice)
#                     .where(text("Invoice.id is null AND message_processed is null"))
#                     .join(
#                         Invoice,
#                         onclause=Message.gmail_message_id == Invoice.gmail_message_id,
#                         isouter=True,
#                     )
#                 )
#             else:
#                 statement = (
#                     select(Message, Invoice)
#                     .where(text("Invoice.id is null AND message_processed is null"))
#                     .join(
#                         Invoice,
#                         onclause=Message.gmail_message_id == Invoice.gmail_message_id,
#                         isouter=True,
#                     )
#                     .limit(qty)
#                 )
#         else:
#             if qty == 0:
#                 statement = (
#                     select(Message, Invoice)
#                     .where(text(sql))
#                     .join(
#                         Invoice,
#                         onclause=Message.gmail_message_id == Invoice.gmail_message_id,
#                         isouter=True,
#                     )
#                 )
#             else:
#                 statement = (
#                     select(Message, Invoice)
#                     .where(text(sql))
#                     .join(
#                         Invoice,
#                         onclause=Message.gmail_message_id == Invoice.gmail_message_id,
#                         isouter=True,
#                     )
#                     .limit(qty)
#                 )
#
#         results = session.exec(statement)
#     return results


# for key in attachments:
#     filename = key
#     _, file_extension = os.path.splitext(filename)
#     filepath = os.path.join(dir_arg, filename)
#     if file_extension.lower() == ".pdf":
#         try:
#             progress.console.print(
#                 f"extracting data from {filepath}"
#             )
#             processed = convert_attachment_to_invoice(
#                 mail_message_id=query, filepath=filepath
#             )
#         except KeyError as error:
#             progress.console.print(f"Key Error: {error}")
#             status = error
#         except ProgrammingError as error:
#             progress.console.print(f"Programming Error: {error}")
#             status = error
#         except DatabaseError as error:
#             progress.console.print(f"Database Error: {error}")
#             status = error
#     if processed:
#         delete_attachment(filepath)
#         total_converted += 1
#     else:
#         total_failed += 1
# update_message_processed_status(result.Message, processed, status)
# progress.console.print(f"{query} processing status is {processed}")
# progress.console.rule()
# progress.advance(task)
# else:
# console.log("no results found")
#
# console.log(f"total converted: {total_converted}\ntotal failed: {total_failed}")


def extract_attachments_from_messages(dir_arg="/tmp/attachments", results=[]):
    for result in results:
        attachments = message_extract_attachments(result.Message.message_raw)
        save_attachment_to_dir(dir_arg=dir_arg, attachments=attachments)
