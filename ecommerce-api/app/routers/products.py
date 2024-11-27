from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import get_db
from app.auth import get_current_user

router = APIRouter()


@router.get("/list", response_model=list[schemas.ProductResponse])
def get_products(category_id: int = None, db: Session = Depends(get_db)):
    if category_id:
        return crud.get_products_by_category(db, category_id)
    return crud.get_all_products(db)


@router.get("/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Update products
@router.post("/create", response_model=schemas.ProductResponse)
def create_product(
        product: schemas.ProductCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    if not current_user.is_seller:
        raise HTTPException(status_code=403, detail="Only sellers can add products")
    return crud.create_product(db, product, seller_id=current_user.id)


