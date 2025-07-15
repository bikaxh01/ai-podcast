from sqlmodel import SQLModel, Field, create_engine
from typing import Optional
from enum import Enum
from dotenv import load_dotenv
from datetime import datetime
import uuid
import os

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")


class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: str
    first_name: str
    avatar_url: Optional[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now())


class Podcast_status(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"


class Podcast(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    description: str
    status: Podcast_status = Field(default=Podcast_status.PENDING)
    audio_url: Optional[str]
    file_url: Optional[str]
    prompt: Optional[str]
    user_id: str = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now())


engine = create_engine(DB_URL)


def connect_Db():
    try:
        SQLModel.metadata.create_all(engine)
        print("DB Connected 🟢")
    except Exception as e:
        print(e)
        raise Exception("Error While Connecting to DB 🔴")
