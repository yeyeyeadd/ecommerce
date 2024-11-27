from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


# User model
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_seller: bool = False


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    # email: EmailStr
    username: str
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


# Produce model
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int
    stock: int


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    seller_id: int

    class Config:
        orm_mode = True


# Order model
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderCreate(BaseModel):
    items: List[OrderItemBase]


class OrderResponse(BaseModel):
    id: int
    buyer_id: int
    total_price: float
    items: List[OrderItemBase]

    class Config:
        orm_mode = True


# Review model
class ReviewBase(BaseModel):
    order_id: int
    rating: int
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewResponse(ReviewBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Category model
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        orm_mode = True


# Token Models (for user authentication)
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
