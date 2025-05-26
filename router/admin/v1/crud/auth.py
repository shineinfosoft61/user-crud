from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy.orm import Session

from libs.utils import verify_password, get_user_by_email


SECRET_KEY = "381836fe163039ab7bcd0a84bf54dded9fbd4269"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db,email)
    if not user or not verify_password(password, user.password):
        return False
    return user
