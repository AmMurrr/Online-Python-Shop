from fastapi import APIRouter, Depends, status, Header
from sqlalchemy.orm import Session
from app.services.auth import AuthService
from app.core.database import get_db
# from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.schemas.auth import UserOut, Signup


router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/signup", status_code=status.HTTP_200_OK, response_model=UserOut)
async def user_login(
        user: Signup,
        db: Session = Depends(get_db)):
    return await AuthService.signup(db, user)


@router.post("/login", status_code=status.HTTP_200_OK,response_model=UserOut)
def user_login(
        username: str,
        password:str,
        db: Session = Depends(get_db)):
    return AuthService.login(username, password, db)


# @router.post("/refresh", status_code=status.HTTP_200_OK)
# async def refresh_access_token(
#         refresh_token: str = Header(),
#         db: Session = Depends(get_db)):
#     return await AuthService.get_refresh_token(token=refresh_token, db=db)
