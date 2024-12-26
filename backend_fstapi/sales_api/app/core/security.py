from fastapi.security.http import HTTPAuthorizationCredentials
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.core.config import settings
from jose import JWTError, jwt
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, Depends, status
from app.models.models import User
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from app.core.database import get_db
from app.utils.responses import ResponseHandler


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_scheme = HTTPBearer()



# Get Payload Of Token
def get_token_payload(token):
    try:
        return jwt.decode(token, settings.secret_key, [settings.algorithm])
    except JWTError:
        raise ResponseHandler.invalid_token('access')



def check_admin_role(
        token: HTTPAuthorizationCredentials = Depends(auth_scheme),
        db: Session = Depends(get_db)):
    user = get_token_payload(token.credentials)
    user_id = user.get('id')
    role_user = db.query(User).filter(User.id == user_id).first()
    if role_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")
