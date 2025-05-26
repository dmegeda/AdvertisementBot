from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter()

class User(BaseModel):
    id: Optional[int] = Field(alias="_id")
    name: str
    contact: str
    role: str

    class Config:
        allow_population_by_field_name = True