from fastapi import APIRouter, Response, HTTPException

from schemas.users import User, LoginUser, PatchUser
from utils import hash_password, verify_password, create_access_token
from database import async_session_maker
from sqlalchemy import delete, insert, select, update
from models.users import UsersOrm
from depends import UserIdDep



router = APIRouter(prefix="/users", tags = ["Авторизация"])

@router.post("/register")
async def register_user(
    data: User
):
    hashed_password = hash_password(data.password)
    new_user_data = User(
        name = data.name, 
        email = data.email,
        password = hashed_password, 
        team_name = data.team_name,
        department_name = data.department_name
    )
    async with async_session_maker() as session:
        add_stat = insert(UsersOrm).values(**new_user_data.model_dump())
        await session.execute(add_stat)
        await session.commit()
    return {'status': 'OK'} 


@router.post("/login")
async def login_user(
    data: LoginUser,
    response: Response
):
    async with async_session_maker() as session:
        query = select(UsersOrm).filter_by(email = data.email)
        res = await session.execute(query)
        user = res.scalars().one()
    if not user:
        raise HTTPException(status_code = 401, detail = "Пользователь с таким email не зарегистрирован")
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Пароль неверный")
    access_token = create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.put("/{user_id}")
async def change_user_put(
    user_id: int,
    current_user_id: UserIdDep, 
    data: User
):
    async with async_session_maker() as session:
        query = select(UsersOrm).filter_by(id = current_user_id)
        result = await session.execute(query)
        current_user = result.scalars().one()
    if user_id != current_user_id and current_user.access_level != "admin":
        raise HTTPException(status_code = 403, detail = "Access denied")
    data.password = hash_password(data.password)
    async with async_session_maker() as session:
        edit_stat = update(UsersOrm).filter_by(id = user_id).values(**data.model_dump())
        await session.execute(edit_stat)
        await session.commit()
    return {'status': 'OK'}


@router.patch("/{user_id}")
async def change_user_access_level(
    user_id: int,
    current_user_id: UserIdDep,
    data: PatchUser
):
    async with async_session_maker() as session:
        query = select(UsersOrm).filter_by(id = current_user_id)
        result = await session.execute(query)
        current_user = result.scalars().one()
    if not current_user.access_level == "admin":
        raise HTTPException(status_code = 403, detail = "Access denied" )
    if data.password:
        data.password = hash_password(data.password)
    async with async_session_maker() as session:
        edit_stat = update(UsersOrm).filter_by(id = user_id).values(**data.model_dump(exclude_unset=True))
        await session.execute(edit_stat)
        await session.commit()
    return {'status': 'OK'}


@router.delete("/{user_id}")
async def delete_user(
    user_id: int, 
    current_user_id: UserIdDep,
):
    async with async_session_maker() as session:
        query = select(UsersOrm).filter_by(id = current_user_id)
        result = await session.execute(query)
        current_user = result.scalars().one()
    if user_id != current_user_id and current_user.access_level != "admin":
        raise HTTPException(status_code = 403, detail = "Access denied")
    async with async_session_maker() as session:
        delete_stat = delete(UsersOrm).filter_by(id = user_id)
        await session.execute(delete_stat)
        await session.commit() 
    return {'status': 'OK'}



@router.get("")
async def get_me(
    user_id: UserIdDep
):
    async with async_session_maker() as session:
        query = select(UsersOrm).filter_by(id = user_id)
        result = await session.execute(query)
        user = result.scalars().one()
    return user

@router.get("/{user_email}")
async def get_user(
    user_email:str
):
    async with async_session_maker() as session:
        query = select(UsersOrm).filter_by(email = user_email)
        result = await session.execute(query)
        user = result.scalars().one()
    return user

