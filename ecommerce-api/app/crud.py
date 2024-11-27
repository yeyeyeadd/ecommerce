from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException


# User managment
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    """create user"""
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=user.password,
        is_seller=user.is_seller
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Category Management
# Get all Categorys
def get_categories(db: Session):
    return db.query(models.Category).all()


# Get Categorys by id
def get_category_by_id(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()


# Create Category
def create_category(db: Session, category: schemas.CategoryCreate):
    new_category = models.Category(name=category.name, description=category.description)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


# Update Category
def update_category(db: Session, category_id: int, category: schemas.CategoryUpdate):
    db_category = get_category_by_id(db, category_id)
    if db_category:
        db_category.name = category.name
        db_category.description = category.description
        db.commit()
        db.refresh(db_category)
        return db_category
    return None


# Delete Category
def delete_category(db: Session, category_id: int):
    db_category = get_category_by_id(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False


# Products Managment
def get_all_products(db: Session):
    return db.query(models.Product).all()


def get_products_by_category(db: Session, category_id: int):
    return db.query(models.Product).filter(models.Product.category_id == category_id).all()


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def create_product(db: Session, product: schemas.ProductCreate, seller_id: int):
    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        category_id=product.category_id,
        seller_id=seller_id,
        stock=product.stock
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# Order Managment
def calculate_order_total(db: Session, order: schemas.OrderCreate):
    """Calculate the total price of the order."""
    total = 0
    for item in order.items:
        product = get_product(db, item.product_id)
        if not product:
            raise ValueError(f"Product with ID {item.product_id} does not exist")
        total += product.price * item.quantity
    return total


def create_order(db: Session, order: schemas.OrderCreate, buyer_id: int, total_price: float):
    """Create order"""
    db_order = models.Order(
        buyer_id=buyer_id,
        total_price=total_price
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order.items:
        db_order_item = models.OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(db_order_item)
    db.commit()
    return db_order


def get_orders_by_user(db: Session, user_id: int):
    """Get user's order"""
    return db.query(models.Order).filter(models.Order.buyer_id == user_id).all()


# Review managment
# Create review
def create_review(db: Session, review: schemas.ReviewCreate, reviewer_id: int):
    new_review = models.Review(
        order_id=review.order_id,
        reviewer_id=reviewer_id,
        rating=review.rating,
        comment=review.comment,
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


# Get item review
def get_reviews_by_order(db: Session, order_id: int):
    return db.query(models.Review).filter(models.Review.order_id == order_id).all()


# Check stock and reduce inventory.
def decrease_stock(db: Session, product_id: int, quantity: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).with_for_update().first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")

    if product.stock < quantity:
        raise HTTPException(status_code=400, detail=f"Insufficient stock for product id {product_id}")

    product.stock -= quantity
    db.add(product)  # mark update


