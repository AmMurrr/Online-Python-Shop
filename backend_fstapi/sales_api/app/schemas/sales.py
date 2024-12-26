from pydantic import BaseModel , EmailStr, validator, Field
from typing import List, Optional
from datetime import datetime
# from app.schemas.carts import CartBase


class BaseConfig:
    from_attributes = True


class SaleItemBase(BaseModel):
    product_id: int
    sale_amount: int


class SaleBase(BaseModel):
    id: int
    user_id: int
    sale_date: datetime
    total_cost: float
    sale_items: List[SaleItemBase]

    class Config(BaseConfig):
        pass

# class SaleBase(BaseModel):
#     id: int
#     username: str
#     email: EmailStr
#     full_name: str
#     password: str
#     role: str
#     is_active: bool
#     created_at: datetime
#     carts: List[CartBase]

#     class Config(BaseConfig):
#         pass


class SaleCreate(BaseModel):
    user_id: int
    total_cost: float
    sale_items: List[SaleItemBase]

    class Config(BaseConfig):
        pass


class SaleOut(BaseModel):
    message: str
    data: SaleBase

    class Config(BaseConfig):
        pass


class SalesOut(BaseModel):
    message: str
    data: List[SaleBase]

    class Config(BaseConfig):
        pass


class SaleOutDelete(BaseModel):
    message: str
    data: SaleBase

    class Config(BaseConfig):
        pass
