import os
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
import time

ACCESS_TOKEN_EXPIRE_MINUTES = 30*60  # 30 minutes
# REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"   # should be kept secret
# JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)

def create_access_token(subject: Union[str, int], expires_delta: int = None) -> str: #todo check type
    if expires_delta is not None:
        expires_delta = time.time() + expires_delta
        
    else:
        expires_delta = time.time() + ACCESS_TOKEN_EXPIRE_MINUTES

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
     
    return encoded_jwt

def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except:
        return {}
