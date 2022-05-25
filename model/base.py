""" This module holds the base SQLModels in use """
import base64
import os
import uuid
from datetime import date
from email import message_from_bytes, policy
from os.path import exists
from typing import List, Optional

import sqlalchemy.exc
from sqlalchemy import text

import pg8000
from invoice2data import extract_data
from invoice2data.extract.loader import read_templates
from pg8000 import DatabaseError, ProgrammingError
from pydantic import UUID4

# from rich import inspect
from rich.console import Console
from rich.progress import Progress
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


class BaseWithUUID(SQLModel):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    deleted_row: bool = Field(index=False, default=False)
