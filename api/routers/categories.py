from fastapi import APIRouter, HTTPException
from typing import List
from db import categories_collection, db
from models.category import Category

router = APIRouter()

def get_next_category_id():
    counter = db.counters.find_one_and_update(
        {"_id": "category_id"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True
    )
    return counter["seq"]

@router.post("/", response_model=Category)
def create_category(category: Category):
    category_dict = category.dict(by_alias=True, exclude={"id"})
    category_dict["_id"] = get_next_category_id()
    categories_collection.insert_one(category_dict)
    return Category(**category_dict)

@router.get("/", response_model=List[Category])
def list_categories():
    categories = list(categories_collection.find())
    return [Category(**cat) for cat in categories]

@router.get("/{category_id}", response_model=Category)
def get_category(category_id: int):
    category = categories_collection.find_one({"_id": category_id})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return Category(**category)

@router.put("/{category_id}", response_model=Category)
def update_category(category_id: int, updated_category: Category):
    updated_dict = updated_category.dict(by_alias=True, exclude={"id"})
    result = categories_collection.update_one(
        {"_id": category_id},
        {"$set": updated_dict}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    return Category(**{**updated_dict, "_id": category_id})

@router.delete("/{category_id}")
def delete_category(category_id: int):
    result = categories_collection.delete_one({"_id": category_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": f"Category {category_id} deleted successfully"}