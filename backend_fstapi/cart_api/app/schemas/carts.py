from pydantic import BaseModel, Field, validator
from typing import List, Optional, ClassVar
from datetime import datetime
# from app.schemas.products import ProductBase, CategoryBase


# Base Config
class BaseConfig:
    from_attributes = True


class CategoryBase(BaseModel):
    id: int
    name: str

class ProductBase(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: int

    @validator("discount_percentage", pre=True)
    def validate_discount_percentage(cls, v):
        if v < 0 or v > 100:
            raise ValueError("discount_percentage must be between 0 and 100")
        return v

    discount_percentage: float
    rating: float
    stock: int
    brand: str
    thumbnail: str
    images: List[str]
    is_published: bool
    created_at: datetime
    category_id: int
    category: CategoryBase

    class Config(BaseConfig):
        pass


class ProductBaseCart(ProductBase):
    category: CategoryBase = Field(exclude=True)

    class Config(BaseConfig):
        pass


# Base Cart & Cart_Item
class CartItemBase(BaseModel):
    id: int
    product_id: int
    quantity: int
    subtotal: float
    product: ProductBaseCart


class CartBase(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    total_amount: float
    cart_items: List[CartItemBase]

    class Config(BaseConfig):
        pass


class CartOutBase(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    total_amount: float
    cart_items: List[CartItemBase]

    class Config(BaseConfig):
        pass


# Get Cart
class CartOut(BaseModel):
    message: str
    data: CartBase

    class Config(BaseConfig):
        pass


class CartsOutList(BaseModel):
    message: str
    data: List[CartBase]


class CartsUserOutList(BaseModel):
    message: str
    data: List[CartBase]

    class Config(BaseConfig):
        pass


# Delete Cart
class CartOutDelete(BaseModel):
    message: str
    data: CartOutBase


# Create Cart
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int


class CartCreate(BaseModel):
    cart_items: List[CartItemCreate]

    class Config(BaseConfig):
        pass


# Update Cart
class CartUpdate(CartCreate):
    pass
