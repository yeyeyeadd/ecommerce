from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import get_db
from app.auth import get_current_user
from loguru import logger
import json


router = APIRouter()


@router.post("/create", response_model=schemas.OrderResponse)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    try:
        # Check and reduce the stock of all products.
        for item in order.items:
            crud.decrease_stock(db, item.product_id, item.quantity)

        # Crate order
        total_price = crud.calculate_order_total(db, order)
        new_order = crud.create_order(db, order, current_user.id, total_price)

        # Return to new order
        return new_order
    except HTTPException as e:
        logger.exception("Create order error", e)
        raise e
    except Exception as e:
        # logger.error("Create order error, order={}", json.dumps(order))
        logger.exception("Create order error", e)
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while processing the order")


@router.get("/list", response_model=list[schemas.OrderResponse])
def get_orders(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_orders_by_user(db, current_user.id)



