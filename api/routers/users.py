from typing import List

from fastapi import APIRouter
from fastapi import HTTPException

from api.db import db, users_collection
from api.lib.user import get_next_user_id

from api.schemas.user import (
    UserCreateSchema,
    UserUpdateSchema,
    UserResponseSchema,
)

router = APIRouter()


@router.post('/', response_model=UserResponseSchema)
def create_user(user: UserCreateSchema):
    user_dict = user.model_dump(by_alias=True, exclude={'id'})
    user_dict['_id'] = get_next_user_id(db)
    users_collection.insert_one(user_dict)
    return UserResponseSchema(**user_dict)


@router.get('/{user_id}', response_model=UserResponseSchema)
def get_user(user_id: int):
    user = users_collection.find_one({'_id': user_id})

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    return UserResponseSchema(**user)


@router.get('/', response_model=List[UserResponseSchema])
def list_users():
    users = users_collection.find()
    return [UserResponseSchema(**user) for user in users]


@router.put('/{user_id}', response_model=UserResponseSchema)
def update_user(user_id: int, updated_user: UserUpdateSchema):
    update_data = updated_user.model_dump(
        by_alias=True,
        exclude_unset=True,
    )
    result = users_collection.update_one(
        filter={'_id': user_id},
        update={'$set': update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail='User not found')

    user = users_collection.find_one({'_id': user_id})
    return UserResponseSchema(**user)


@router.delete('/{user_id}')
def delete_user(user_id: int):
    result = users_collection.delete_one({'_id': user_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail='User not found')

    return {'message': f'User {user_id} deleted successfully'}
