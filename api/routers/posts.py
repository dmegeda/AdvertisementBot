from fastapi import APIRouter, HTTPException
from typing import List
from db import posts_collection
from models.post import Post
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=Post)
def create_post(post: Post):
    post_dict = post.dict(by_alias=True, exclude={"id"})
    post_dict["_id"] = ObjectId()
    posts_collection.insert_one(post_dict)
    
    post_dict["_id"] = str(post_dict["_id"])
    return post_dict

@router.get("/", response_model=List[Post])
def list_posts():
    posts = list(posts_collection.find())
    for post in posts:
        post["_id"] = str(post["_id"])
    return posts

@router.get("/{post_id}", response_model=Post)
def get_post(post_id: str):
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post["_id"] = str(post["_id"])
    return post

@router.put("/{post_id}", response_model=Post)
def update_post(post_id: str, updated_post: Post):
    updated_dict = updated_post.dict(exclude={"id"})

    result = posts_collection.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": updated_dict}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return {**updated_dict, "_id": post_id}

@router.delete("/{post_id}")
def delete_post(post_id: str):
    result = posts_collection.delete_one({"_id": ObjectId(post_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": f"Post {post_id} deleted successfully"}