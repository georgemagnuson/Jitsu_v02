import os
import pickle
import uuid
from configparser import ConfigParser
from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import UUID4
from rich.console import Console
from rich.progress import Progress
from sqlmodel import Field, Session, SQLModel, create_engine, select

# from sqlalchemy.dialects.postgresql import UUID
# from flask_sqlalchemy import SQLAlchemy

import pg8000


class Message(SQLModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    gmail_message_id: str
    message_date: date
    message_from: str
    message_to: str
    message_subject: str
    message_has_attachments: bool
    deleted_row: bool
    message_raw: str


# sqlite database
# sqlite_file_name = "database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"
# engine = create_engine(sqlite_url, echo=True)

# postgresql database
pg_file_name = "jitsu_dev"
pg_url = "postgresql+pg8000://{}:{}@{}:{}/{}".format(
    "jitsu_dev", "rash4z4m!", "165.227.70.211", 5432, pg_file_name
)
engine = create_engine(pg_url, echo=True)
# engine = create_engine(PG_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Create message
def create_message(
    gmessage_id,
    gmessage_date,
    gmessage_from,
    gmessage_to,
    gmessage_subject,
    gmessage_has_attachments,
    gmessage_raw,
):
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


def save_message_to_postgresql(self):
    console = Console()
    if select_first_message(self.message_id):
        console.log(
            f"[bright_yellow]WARNING: message id [white]{self.message_id}[/white] already exists."
        )
    else:
        create_message(
            self.message_id,
            self.message_date,
            self.message_from,
            self.message_to,
            self.message_subject,
            self.message_has_attachment,
            self.message_raw,
        )

    console.log("adding SupplierMail/InvoicesProcessed label")
    # SupplierMail/InvoicesProcessed
    self.message_label_add("Label_6569528190372695776")
    console.log("removing SupplierMail/InvoicesNew label")
    # SupplierMail/InvoicesNew
    self.message_label_remove("Label_6976860208836301729")
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


# Read all message
def select_all_message():
    with Session(engine) as session:
        statement = select(Message)
        # .where( Message.gmail_message_id = gmessage_id)
        results = session.exec(statement)
        return results


# Read all message with sql
def select_all_message_with(sql: str):
    with Session(engine) as session:
        statement = select(Message).where(sql)
        results = session.exec(statement)
        return results


# Read one message
def select_first_message(gmessage_id: str):
    with Session(engine) as session:
        statement = select(Message).where(Message.gmail_message_id == gmessage_id)
        results = session.exec(statement)
        message_1 = results.first()
        return message_1


# Update message


# Delete message


def main():
    create_db_and_tables()
    return


if __name__ == "__main__":
    main()
