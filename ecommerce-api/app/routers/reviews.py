from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.models import User
from app.database import get_db
from app.auth import get_current_user
from typing import List

router = APIRouter()


# Create review
@router.post("/create", response_model=schemas.ReviewResponse)
def create_review(
        review: schemas.ReviewCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return crud.create_review(db, review, current_user.id)


# Get review
@router.get("/{order_id}", response_model=List[schemas.ReviewResponse])
def get_reviews(order_id: int, db: Session = Depends(get_db)):
    reviews = crud.get_reviews_by_order(db, order_id)
    if not reviews:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No reviews found")
    return reviews


