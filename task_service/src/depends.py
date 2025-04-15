from fastapi import Request,  HTTPException, Depends
import httpx

from config import settings

async def get_current_user(request: Request):
    async with httpx.AsyncClient(cookies=request.cookies) as session:
        resp = await session.get(f"http://{settings.USERS_SERVICE_HOST}:{settings.USERS_SERVICE_PORT}/users/me")
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Неавторизован")
        return resp.json()
    
async def is_head_role(user: dict = Depends(get_current_user)):
    if user["role"] != "head":
        raise HTTPException(status_code=403, detail="Вы не являетесь руководителем")
    return user