from fastapi import APIRouter
from models.departments import DepartmentsOrm
from schemas.departments import Department, DepratmentPatch
from database import async_session_maker
from sqlalchemy import insert, update

router = APIRouter(prefix="/departments", tags=["Администрирование отделов"])

@router.post("/register")
async def register_departments(
    data: Department
):
    async with async_session_maker() as session:
        add_stat = insert(DepartmentsOrm).values(**data.model_dump())
        await session.execute(add_stat)
        await session.commit() 
    return {'status': 'OK'} 

@router.put("/{dep_id}")
async def edit_derpartments(
    dep_id : int,
    dep_data: Department
):
    async with async_session_maker() as session:
        edit_stat = update(DepartmentsOrm).filter_by(id = dep_id).values(**dep_data.model_dump())
        await session.execute(edit_stat)
        await session.commit() 
    return {'status': 'OK'} 

@router.patch("/{dep_id}")
async def edit_departments_partially(
    dep_id: int,
    dep_data: DepratmentPatch
):
    async with async_session_maker() as session:
        edit_stat = update(DepartmentsOrm).filter_by(id = dep_id).values(**dep_data.model_dump(exclude_unset=True))
        await session.execute(edit_stat)
        await session.commit() 
    return {'status': 'OK'} 