from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class Attachment(BaseModel):
    file_type: str
    url: str


class Comment(BaseModel):
    user_id: int
    text: str
    timestamp: datetime


class Post(BaseModel):
    id: int = Field(alias="_id")  # Required because "_id" is required in MongoDB
    title: str
    description: str
    category_id: int
    message_id: str
    chat_msg_id: str
    author_id: int
    created_at: datetime
    attachments: List[Attachment]
    comments: List[Comment]

    class Config:
        allow_population_by_field_name = True