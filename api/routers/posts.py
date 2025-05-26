from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException

from api.db import db, posts_collection
from api.lib.post import get_next_post_id
from api.schemas.post import (
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


@router.get("/{post_id}", response_model=PostResponseSchema)
def get_post(post_id: int):
    post = posts_collection.find_one({"_id": post_id})

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return PostResponseSchema(**post)


@router.put("/{post_id}", response_model=PostResponseSchema)
def update_post(post_id: int, updated_post: PostUpdateSchema):
    updated_dict = updated_post.model_dump(by_alias=True)
    result = posts_collection.update_one(
        {"_id": post_id},
        {"$set": updated_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")

    post = posts_collection.find_one({"_id": post_id})
    return PostResponseSchema(**post)


@router.delete("/{post_id}")
def delete_post(post_id: int):
    result = posts_collection.delete_one({"_id": post_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"message": f"Post {post_id} deleted successfully"}
