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


@router.get("/name/{name}", response_model=CategoryResponseSchema)
def get_category(name: str):
    category = categories_collection.find_one({"name": name})

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


@router.delete("/{name}")
def delete_category(name: str):
    result = categories_collection.delete_one({"name": name})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")

    return {"message": f"Category {name} deleted successfully"}
