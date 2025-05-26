from pydantic import BaseModel, Field


class Category(BaseModel):
    id: int = Field(alias="_id")
    name: str

    class Config:

        allow_population_by_field_name = True
