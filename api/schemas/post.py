from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PostAttachment(BaseModel):
    file_type: str
    url: str


class PostComment(BaseModel):
    user_id: int
    text: str
    timestamp: datetime


class PostCreateSchema(BaseModel):
    title: str
    description: str
    category_id: int
    author_id: int
    attachments: List[PostAttachment] = Field(default_factory=list)
    comments: List[PostComment] = Field(default_factory=list)

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True


class PostUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    attachments: Optional[List[PostAttachment]] = None
    comments: Optional[List[PostComment]] = None

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True


class PostResponseSchema(BaseModel):
    id: int = Field(alias="_id")
    title: str
    description: str
    category_id: int
    author_id: int
    created_at: datetime
    attachments: List[PostAttachment]
    comments: List[PostComment]

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True
