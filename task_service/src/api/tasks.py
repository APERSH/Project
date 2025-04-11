from fastapi import APIRouter, Request, HTTPException
import httpx

from schemas.tasks import CreateTask, PatchTask
from database import async_session_maker
from sqlalchemy import insert, update, delete, select
from models.tasks import TasksOrm


router = APIRouter(prefix="/tasks", tags = ["Задачи"])

@router.post("/register")
async def register_tasks(
    request: Request,
    task_data: CreateTask
):
    async with httpx.AsyncClient(cookies=request.cookies) as session:
        creator_resp = await session.get(f"http://localhost:8000/users") 
        creator =  creator_resp.json()
        executor_resp = await session.get(f"http://localhost:8000/users/{task_data.executor_email}")
        executor =  executor_resp.json()
    if not creator["role"] == "head":
        raise HTTPException(status_code = 403, detail = "Вы не являетесь руководителем")
    if not creator["team_name"] == executor["team_name"]:
        raise HTTPException(status_code = 403, detail = "Нельзя назначить задачу сотруднику другой команды")
    if not creator["department_name"] == executor["department_name"]:
        raise HTTPException(status_code = 403, detail = "Нельзя назначить задачу сотруднику другого отдела")
    async with async_session_maker() as session:
        add_stat = insert(TasksOrm).values(**task_data.model_dump())
        await session.execute(add_stat)
        await session.commit()
    return {'status': 'OK'} 


@router.patch("/{task_id}")
async def edit_task(
    request: Request,
    task_id: int,
    task_data: PatchTask
):
    async with httpx.AsyncClient(cookies=request.cookies) as session:
        creator_resp = await session.get(f"http://localhost:8000/users") 
        creator =  creator_resp.json()
    if not creator["role"] == "head":
        raise HTTPException(status_code = 403, detail = "Вы не являетесь руководителем")
    async with async_session_maker() as session:
        edit_stat = update(TasksOrm).filter_by(id = task_id).values(**task_data.model_dump(exclude_unset = True))
        await session.execute(edit_stat)
        await session.commit()
    return {'status': 'OK'}


@router.delete("/{task_id}")
async def  delete_task(
    task_id: int,
    request: Request
):
    async with httpx.AsyncClient(cookies=request.cookies) as session:
        creator_resp = await session.get(f"http://localhost:8000/users") 
        creator =  creator_resp.json()
    if not creator["role"] == "head":
        raise HTTPException(status_code = 403, detail = "Вы не являетесь руководителем")
    async with async_session_maker() as session:
        delete_stat = delete(TasksOrm).filter_by(id = task_id)
        await session.execute(delete_stat)
        await session.commit()
    return {'status': 'OK'}


@router.get("/{task_id}")
async def get_task_by_id(
    task_id: int
):
    async with async_session_maker() as session:
        query = select(TasksOrm).filter_by(id = task_id)
        res = await session.execute(query)
    return res.scalars().one_or_none()


@router.get("")
async def get_tasks(
    executor_email: str  
):
    async with async_session_maker() as session:
        query = select(TasksOrm).filter_by(executor_email = executor_email)
        res = await session.execute(query)
    return res.scalars().all()




