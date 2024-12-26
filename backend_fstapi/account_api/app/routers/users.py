from fastapi import APIRouter, Depends, Query, status
from app.core.database import get_db
from app.services.users import UserService
from sqlalchemy.orm import Session
from app.schemas.users import UserCreate, UserOut, UsersOut, UserOutDelete, UserUpdate
# from app.core.security import check_admin_role


router = APIRouter(tags=["Users"], prefix="/users")


# Get All Users
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=UsersOut)
def get_all_users(
    db: Session = Depends(get_db)
):
    return UserService.get_all_users(db)


# Get User By ID
@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return UserService.get_user(db, user_id)


# Create New User
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db, user)


# # Update Existing User
# @router.put(
#     "/{user_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=UserOut,
#     dependencies=[Depends(check_admin_role)])
# def update_user(user_id: int, updated_user: UserUpdate, db: Session = Depends(get_db)):
#     return UserService.update_user(db, user_id, updated_user)


# Delete User By ID
@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserOutDelete)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return UserService.delete_user(db, user_id)
