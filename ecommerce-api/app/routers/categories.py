from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db
from app.models import User
from typing import List
from app.auth import get_current_user
import os


router = APIRouter()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")


# Get all Category
@router.get("/list", response_model=List[schemas.CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    categories = crud.get_categories(db)
    return categories


# Get single Category
@router.get("/{category_id}", response_model=schemas.CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


# Create a Category (admin require)
@router.post("/create", response_model=schemas.CategoryResponse)
def create_category(
        category: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    # if not current_user.is_seller:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    if current_user.username != ADMIN_USERNAME:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return crud.create_category(db, category)


# Update Category info (admin require)
@router.put("/{category_id}", response_model=schemas.CategoryResponse)
def update_category(
        category_id: int,
        category: schemas.CategoryUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    # if not current_user.is_seller:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    if current_user.username != ADMIN_USERNAME:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    updated_category = crud.update_category(db, category_id, category)
    if not updated_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return updated_category


# delete Category (admin require)
@router.delete("/{category_id}")
def delete_category(
        category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    # if not current_user.is_seller:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    if current_user.username != ADMIN_USERNAME:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    deleted = crud.delete_category(db, category_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return {"message": "Category deleted successfully"}
