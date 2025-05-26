from typing import List

from fastapi import APIRouter, HTTPException

from api.db import categories_collection, db
from api.lib.category import get_next_category_id
from api.schemas.category import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema,
)

router = APIRouter()


@router.post("/", response_model=CategoryResponseSchema)
def create_category(category: CategoryCreateSchema):
    category_dict = category.model_dump(by_alias=True)
    category_dict["_id"] = get_next_category_id(db)
    categories_collection.insert_one(category_dict)
    return CategoryResponseSchema(**category_dict)


@router.get("/{category_id}", response_model=CategoryResponseSchema)
def get_category(category_id: int):
    category = categories_collection.find_one({"_id": category_id})

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return CategoryResponseSchema(**category)


@router.get("/", response_model=List[CategoryResponseSchema])
def list_categories():
    categories = list(categories_collection.find())
    return [CategoryResponseSchema(**cat) for cat in categories]


@router.put("/{category_id}", response_model=CategoryResponseSchema)
def update_category(category_id: int, updated_category: CategoryUpdateSchema):
    updated_dict = updated_category.model_dump(by_alias=True)
    result = categories_collection.update_one(
        {"_id": category_id},
        {"$set": updated_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")

    category = categories_collection.find_one({"_id": category_id})
    return CategoryResponseSchema(**category)


@router.delete("/{category_id}")
def delete_category(category_id: int):
    result = categories_collection.delete_one({"_id": category_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")

    return {"message": f"Category {category_id} deleted successfully"}
