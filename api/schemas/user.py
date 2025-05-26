from pydantic import BaseModel, Field

from api.models.user import UserRole


class UserCreateSchema(BaseModel):
    name: str
    contact: str
    role: UserRole

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True


class UserUpdateSchema(BaseModel):
    name: str | None = None
    contact: str | None = None
    role: UserRole

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True


class UserResponseSchema(BaseModel):
    id: int = Field(alias="_id")
    name: str
    contact: str
    role: UserRole

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True
