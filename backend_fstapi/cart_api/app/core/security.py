# from fastapi.security.http import HTTPAuthorizationCredentials
# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# from app.core.config import settings
# from jose import JWTError, jwt
# #from app.schemas.auth import TokenResponse
# from fastapi.encoders import jsonable_encoder
# from fastapi import HTTPException, Depends, status
# from app.models.models import User
# from sqlalchemy.orm import Session
# from fastapi.security import HTTPBearer
# from app.core.database import get_db
# from app.utils.responses import ResponseHandler


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# auth_scheme = HTTPBearer()



# # Get Payload Of Token
# def get_token_payload(token):
#     try:
#         return jwt.decode(token, settings.secret_key, [settings.algorithm])
#     except JWTError:
#         raise ResponseHandler.invalid_token('access')


# def get_current_user(token):
#     user = get_token_payload(token.credentials)
#     return user.get('id')



