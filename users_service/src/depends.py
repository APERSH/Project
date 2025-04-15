import jwt

from typing import Annotated

from database import async_session_maker
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from config import settings
from fastapi import Request, HTTPException, Depends

async def get_db() ->AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


def get_current_user_id(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code = 401, detail="Вы не предоставли токен доступа")
    try:
        data = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code = 401, detail = "Неверный токен") 
    return data["user_id"]

UserIdDep = Annotated[int, Depends(get_current_user_id)]