from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException
from pymongo import DESCENDING

from db import db, posts_collection
from lib.post import get_next_post_id
from schemas.post import (
    PostCreateSchema,
    PostUpdateSchema,
    PostResponseSchema,
)


router = APIRouter()


@router.post("/", response_model=PostResponseSchema)
def create_post(post: PostCreateSchema):
    post_dict = post.model_dump(by_alias=True)
    post_dict["_id"] = get_next_post_id(db)
    post_dict["created_at"] = datetime.now()
    posts_collection.insert_one(post_dict)
    return PostResponseSchema(**post_dict)


@router.get("/", response_model=List[PostResponseSchema])
def list_posts():
    posts = list(posts_collection.find())
    return [PostResponseSchema(**post) for post in posts]

@router.get("/author/{author_id}", response_model=List[PostResponseSchema])
def list_posts(author_id: int):
    posts = list(posts_collection.find(
        {"author_id": author_id},
        sort=[("created_at", DESCENDING)]
    ))
    return [PostResponseSchema(**post) for post in posts]

@router.get("/{message_id}", response_model=PostResponseSchema)
def get_post(message_id: str):
    post = posts_collection.find_one({"message_id": message_id})

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return PostResponseSchema(**post)

@router.get("/thread/{chat_msg_id}", response_model=PostResponseSchema)
def get_post(chat_msg_id: str):
    post = posts_collection.find_one({"chat_msg_id": chat_msg_id})

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return PostResponseSchema(**post)

@router.get("/last/{author_id}", response_model=PostResponseSchema)
def get_post(author_id: int):
    post = posts_collection.find_one(
        {"author_id": author_id},
        sort=[("created_at", DESCENDING)]
    )

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return PostResponseSchema(**post)


@router.put("/{message_id}", response_model=PostResponseSchema)
def update_post(message_id: str, updated_post: PostUpdateSchema):
    updated_dict = updated_post.model_dump(by_alias=True)
    result = posts_collection.update_one(
        {"message_id": message_id},
        {"$set": updated_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")

    post = posts_collection.find_one({"message_id": message_id})
    return PostResponseSchema(**post)


@router.delete("/{message_id}")
def delete_post(message_id: str):
    result = posts_collection.delete_one({"message_id": message_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"message": f"Post {message_id} deleted successfully"}
