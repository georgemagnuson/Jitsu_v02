import base64
import os
import uuid
from datetime import date
from email import message_from_bytes, policy
from os.path import exists
from typing import List, Optional

import pydantic
from pydantic import UUID4
from rich.console import Console
from rich.progress import Progress
from sqlmodel import (Field, Relationship, Session, SQLModel, create_engine,
                      select)

import base

PG_FILE_NAME = "jitsu_dev"
PG_URL = "postgresql+pg8000://{}:{}@{}:{}/{}".format(
    "jitsu_dev", "rash4z4m!", "165.227.70.211", 5432, PG_FILE_NAME
)
# engine = create_engine(PG_URL, echo=True)
engine = create_engine(PG_URL)


def create_db_and_tables():
    """run SQLModel to create database and table"""
    SQLModel.metadata.create_all(engine)


def create_message(
    gmessage_id: UUID4,
    gmessage_date: date,
    gmessage_from: str,
    gmessage_to: str,
    gmessage_subject: str,
    gmessage_has_attachments: bool,
    gmessage_raw: str,
):
    """extracted gmail info saved as postgresql message"""
    message_1 = Message(
        gmail_message_id=gmessage_id,
        message_date=gmessage_date,
        message_from=gmessage_from,
        message_to=gmessage_to,
        message_subject=gmessage_subject,
        message_has_attachments=gmessage_has_attachments,
        message_raw=gmessage_raw,
    )

    with Session(engine) as session:
        session.add(message_1)

        session.commit()


class Message(base.BaseWithUUID, table=True):
    """this holds the gmail_message class"""

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


def update_message_processed_status(message: Message, processed: bool, status: str):
    """update message"""
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
    """return email object from raw_mail"""
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
    """Delete attachments after successful invoice2data"""
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


def select_first_message(gmessage_id: str):
    """Read one message"""
    with Session(engine) as session:
        statement = select(Message).where(Message.gmail_message_id == gmessage_id)
        results = session.exec(statement)
        message_1 = results.first()
        return message_1


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
#                 gmessage_id=query, filepath=filepath
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
