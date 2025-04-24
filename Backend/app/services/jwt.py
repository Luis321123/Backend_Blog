from fastapi import HTTPException
from datetime import  timedelta

import logging

from app.utils.string import unique_string
from app.core.security import get_token_payload, str_decode, str_encode, generate_token
from app.core.settings import get_settings

settings = get_settings()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _generate_tokens(user):
        refresh_key = unique_string(100)
        access_key = unique_string(50)
        rt_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

        user_data = {
            "name": user.name,
            "last_name": user.last_name,
            "email": user.email,
        
        }

        at_payload = {
            "sub": str_encode(str(user.uuid)),
            'a': access_key,
            'r': str_encode(str(user.uuid)),
            'n': str_encode(f"{user_data}")
        }

        at_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = generate_token(at_payload, settings.JWT_SECRET, settings.JWT_ALGORITHM, at_expires)

        rt_payload = {
             "sub": str_encode(str(user.uuid)),
             "t": refresh_key,
             'a': access_key
        }
        refresh_token = generate_token(rt_payload, settings.SECRET_KEY, settings.JWT_ALGORITHM, rt_expires)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": at_expires.seconds,
            'refresh_expires_in': rt_expires.seconds
        }

async def get_refresh_token(refresh_token, db):
    from app.models.User import User
    
    token_payload = get_token_payload(refresh_token, settings.SECRET_KEY, settings.JWT_ALGORITHM)
    if not token_payload:
        raise HTTPException(status_code=400, detail="Invalid refresh token")

    user_uuid = str_decode(str(token_payload.get('sub')))
    user = db.query(User).filter(User.uuid == user_uuid).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return _generate_tokens(user)