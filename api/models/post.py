from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

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
    author_id: int
    created_at: datetime
    attachments: List[Attachment]
    comments: List[Comment]

    class Config:
        allow_population_by_field_name = True