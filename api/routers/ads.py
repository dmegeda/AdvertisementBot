from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from db import ads_collection

router = APIRouter()

class Attachment(BaseModel):
    file_type: str
    url: str

class Comment(BaseModel):
    user_id: int
    text: str
    timestamp: str

class Ad(BaseModel):
    title: str
    description: str
    category: str
    author_id: int
    created_at: str
    attachments: Optional[List[Attachment]] = []
    comments: Optional[List[Comment]] = []

@router.post("/", response_model=Ad)
def create_ad(ad: Ad):
    ads_collection.insert_one(ad.dict())
    return ad

@router.get("/", response_model=List[Ad])
def list_ads():
    return list(ads_collection.find({}, {"_id": 0}))