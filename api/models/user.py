from enum import Enum

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class UserRole(str, Enum):
    user = "user"
    admin = "admin"


class User(BaseModel):
    id: int = Field(alias="_id")
    name: str
    contact: str
    role: UserRole

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True
