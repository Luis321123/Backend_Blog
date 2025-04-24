from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import logging
import jwt
from passlib.context import CryptContext
import base64

from datetime import datetime, timedelta
from app.core.settings import get_settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SPECIAL_CHARACTERS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>']

settings = get_settings()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password: str) -> str: 
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def is_password_strong_enough(password: str) -> bool:
    if len(password) < 8:
        return False

    if not any(char.isupper() for char in password):
        return False

    if not any(char.islower() for char in password):
        return False

    if not any(char.isdigit() for char in password):
        return False

    if not any(char in SPECIAL_CHARACTERS for char in password):
        return False

    return True

def str_encode(string: str) -> str:
    return base64.b85encode(string.encode('utf-8')).decode('utf-8')


def str_decode(string: str) -> str:
    return base64.b85decode(string.encode('utf-8')).decode('utf-8')

def get_token_payload(token: str, secret: str, algo: str):
    payload = jwt.decode(token, secret, algorithms=algo)
    return payload

def generate_token(payload: dict, secret: str, algo: str, expiry: timedelta):
    expire = datetime.now() + expiry
    payload.update({"exp": expire})
    return jwt.encode(payload, secret, algorithm=algo)

async def get_token_user(token: str, db= Session):
    from app.models.User import User
    payload = get_token_payload(token, settings.JWT_SECRET, settings.JWT_ALGORITHM)
    if payload: 
        user_uuid = str_decode(str(payload.get('sub')))
        user = db.query(User).filter(User.uuid == user_uuid).first()
        
        if user: 
            return user
    return None

async def load_user(email: str, db= Session):
    from app.models.User import User
    try:
        user = Session.query(User).filter(User.email == email).first()
    except Exception as user_exec:
        user = None
    return user
