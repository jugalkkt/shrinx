from fastapi import Cookie, HTTPException, Depends
from app.models import User
from app.core.jwt import decode_token
import jwt as pyjwt


async def current_user_optional(session: str | None = Cookie(default=None)) -> User | None:
    if session is None:
        return None
    try:
        payload = decode_token(session)
    except pyjwt.ExpiredSignatureError:
        return None
    except pyjwt.InvalidTokenError:
        return None
    user = await User.get(payload["sub"])
    return user

async def current_user_required(user: User | None = Depends(current_user_optional)) -> User:
    if user is None:
        raise HTTPException(status_code=401)
    return user