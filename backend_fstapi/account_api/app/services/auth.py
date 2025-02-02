from fastapi import HTTPException, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.models import User
from app.core.database import get_db
from app.core.security import verify_password#, get_user_token, get_token_payload
from app.core.security import get_password_hash
from app.utils.responses import ResponseHandler
from app.schemas.auth import Signup





class AuthService:
    @staticmethod
    def login(username, password, db: Session ):
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

        if not verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

        return ResponseHandler.get_single_success(user.username, user.id, user)

    @staticmethod
    async def signup(db: Session, user: Signup):
        hashed_password = get_password_hash(user.password)
        user.password = hashed_password
        db_user = User(id=None, **user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return ResponseHandler.create_success(db_user.username, db_user.id, db_user)

    # @staticmethod
    # async def get_refresh_token(token, db):
    #     payload = get_token_payload(token)
    #     user_id = payload.get('id', None)
    #     if not user_id:
    #         raise ResponseHandler.invalid_token('refresh')

    #     user = db.query(User).filter(User.id == user_id).first()
    #     if not user:
    #         raise ResponseHandler.invalid_token('refresh')

    #     return await get_user_token(id=user.id, refresh_token=token)
