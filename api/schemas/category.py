from pydantic import BaseModel, Field
from typing import Optional


class CategoryCreateSchema(BaseModel):
    name: str

    class Config:
        allow_population_by_field_name = True


class CategoryUpdateSchema(BaseModel):
    name: Optional[str] = None

    class Config:
        allow_population_by_field_name = True


class CategoryResponseSchema(BaseModel):
    id: int = Field(alias="_id")
    name: str

    class Config:
        allow_population_by_field_name = True
