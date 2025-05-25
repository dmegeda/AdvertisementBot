from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from db import users_collection

router = APIRouter()

class User(BaseModel):
    name: str
    contact: str

@router.post("/", response_model=User)
def create_user(user: User):
    users_collection.insert_one(user.dict())
    return user

@router.get("/", response_model=List[User])
def list_users():
    return list(users_collection.find({}, {"_id": 0}))