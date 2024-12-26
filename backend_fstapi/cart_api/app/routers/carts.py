from fastapi import APIRouter, Depends, Query, status
from app.core.database import get_db
from app.services.carts import CartService
from sqlalchemy.orm import Session
from app.schemas.carts import CartCreate, CartUpdate, CartOut, CartOutDelete, CartsOutList
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

router = APIRouter(tags=["Carts"], prefix="/carts")
auth_scheme = HTTPBearer()


# Get All Carts
@router.get("/", status_code=status.HTTP_200_OK, response_model=CartsOutList)
def get_all_carts(
    db: Session = Depends(get_db),
):
    return CartService.get_all_carts( db)


# Get Cart By User ID
@router.get("/{cart_id}", status_code=status.HTTP_200_OK, response_model=CartOut)
def get_cart(
        # cart_id: int,
        user_id: int,
        db: Session = Depends(get_db)
        ):
    return CartService.get_cart(user_id, db)#, cart_id)


# Create New Cart
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CartOut)
def create_cart(
        user_id: int,
        cart: CartCreate, db: Session = Depends(get_db),
        ):
    return CartService.create_cart(user_id, db, cart)


# Update Existing Cart
@router.put("/{cart_id}", status_code=status.HTTP_200_OK, response_model=CartOut)
def update_cart(
        user_id: int,
        updated_cart: CartUpdate,
        db: Session = Depends(get_db),
        ):
    return CartService.update_cart(user_id, db, updated_cart)


# Delete Cart By User ID
@router.delete("/{cart_id}", status_code=status.HTTP_200_OK, response_model=CartOutDelete)
def delete_cart(
       user_id: int, db: Session = Depends(get_db),
        ):
    return CartService.delete_cart(user_id, db)
