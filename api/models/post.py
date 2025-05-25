from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Attachment(BaseModel):
    file_type: str
    url: str

class Comment(BaseModel):
    user_id: int
    text: str
    timestamp: datetime

class Post(BaseModel):
    id: Optional[str] = Field(alias="_id")
    title: str
    description: str
    category_id: str
    author_id: int
    created_at: datetime
    attachments: Optional[List[Attachment]] = []
    comments: Optional[List[Comment]] = []