# file for jwt token operations

from jose import JWTError, jwt
from datetime import datetime
from schemas.user import TokenData
from core.config import Settings

SECRET_KEY = Settings.SECRET_KEY
ALGORITHM = Settings.ALGORITHM

def get_attribute(token: str, attribute: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name = payload.get(attribute)
        return name
    except JWTError:
        return None

def get_data(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_data = TokenData(
            sub=payload.get("sub"),
            name=payload.get("name"),
            nationality=payload.get("nationality"),
            role=payload.get("role"),
        )
        return user_data
    except JWTError:
        return None

def is_token_expired(payload: dict) -> bool:
    exp = payload.get("exp")
    if exp:
        return datetime.fromtimestamp(exp) < datetime.now()
    return True