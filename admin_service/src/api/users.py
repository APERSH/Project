from fastapi import APIRouter, Request
import httpx

from schemas.users import EditUser, User

router = APIRouter(prefix="/users", tags = ["Администрирование пользователей"])

@router.get("")
async def get_user(request: Request):
    async with httpx.AsyncClient(cookies=request.cookies) as session:
        resp = await session.get(f"http://localhost:8000/users") 
        return resp.json() 


@router.post("/register")
async def register_user(
    request: Request,
    data: User
):
    async with httpx.AsyncClient(cookies=request.cookies) as session:
        res = await session.post(
            f"http://localhost:8000/users/register",
            json = data.model_dump())
        return res.json()

@router.put("/{user_id}")
async def edit_user(
    user_id: int,
    request: Request,
    data: User
):
    async with httpx.AsyncClient(cookies=request.cookies) as session:
        res = await session.put(
            f"http://localhost:8000/users/{user_id}",
            json = data.model_dump()
        )
        return res.json()

@router.patch("/{user_id}")
async def edit_user(
    user_id: int,
    request: Request,
    data: EditUser
):
    async with httpx.AsyncClient(cookies=request.cookies) as session:
        res = await session.patch(
            f"http://localhost:8000/users/{user_id}", 
            json = data.model_dump(exclude_unset=True))
        return res.json() 
    

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    request: Request
):
    async with httpx.AsyncClient(cookies=request.cookies) as session:
        res = await session.delete(f"http://localhost:8000/users/{user_id}")
        return res.json()
    

@router.get("/{user_email}")
async def get_user_by_email(
    user_email: str
):
    async with httpx.AsyncClient() as session:
        res = await session.get(f"http://localhost:8000/users/{user_email}")
        return res.json()