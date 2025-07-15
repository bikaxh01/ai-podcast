from sqlmodel import SQLModel
from typing import Optional
from Db.db import Podcast_status


class Podcast_model(SQLModel):
    title: Optional[str]  = None
    description: Optional[str] = None
    status: Optional[Podcast_status] = None
    audio_url: Optional[str] = None
    file_url: Optional[str]  = None
    prompt: str
