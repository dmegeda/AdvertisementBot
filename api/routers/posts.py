from fastapi import APIRouter, HTTPException
from typing import List
from db import posts_collection, db
from models.post import Post

router = APIRouter()

def get_next_post_id():
    counter = db.counters.find_one_and_update(
        {"_id": "post_id"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True
    )
    return counter["seq"]

@router.post("/", response_model=Post)
def create_post(post: Post):
    post_dict = post.dict(by_alias=True, exclude={"id"})
    post_dict["_id"] = get_next_post_id()
    posts_collection.insert_one(post_dict)
    return Post(**post_dict)

@router.get("/", response_model=List[Post])
def list_posts():
    posts = list(posts_collection.find())
    return [Post(**post) for post in posts]

@router.get("/{post_id}", response_model=Post)
def get_post(post_id: int):
    post = posts_collection.find_one({"_id": post_id})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return Post(**post)

@router.put("/{post_id}", response_model=Post)
def update_post(post_id: int, updated_post: Post):
    updated_dict = updated_post.dict(by_alias=True, exclude={"id"})
    result = posts_collection.update_one(
        {"_id": post_id},
        {"$set": updated_dict}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    return Post(**{**updated_dict, "_id": post_id})

@router.delete("/{post_id}")
def delete_post(post_id: int):
    result = posts_collection.delete_one({"_id": post_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": f"Post {post_id} deleted successfully"}