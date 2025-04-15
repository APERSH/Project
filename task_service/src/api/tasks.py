from fastapi import APIRouter, Request, HTTPException, Depends
import httpx

from schemas.tasks import CreateTask, PatchTask
from database import async_session_maker
from sqlalchemy import insert, update, delete, select
from models.tasks import TasksOrm
from config import settings
from depends import is_head_role, get_current_user


router = APIRouter(prefix="/tasks", tags = ["Задачи"])

@router.post("/register")
async def register_tasks(
    request: Request,
    task_data: CreateTask, 
    creator: dict = Depends(is_head_role)
):
    async with httpx.AsyncClient(cookies=request.cookies) as session:
        executor_resp = await session.get(f"http://{settings.USERS_SERVICE_HOST}:{settings.USERS_SERVICE_PORT}/users/{task_data.executor_email}")
        executor =  executor_resp.json()
    if not creator["team_id"] == executor["team_id"]:
        raise HTTPException(status_code = 403, detail = "Нельзя назначить задачу сотруднику другой команды")
    if not creator["department_id"] == executor["department_id"]:
        raise HTTPException(status_code = 403, detail = "Нельзя назначить задачу сотруднику другого отдела")
    async with async_session_maker() as session:
        add_stat = insert(TasksOrm).values(**task_data.model_dump(exclude_unset = True))
        await session.execute(add_stat)
        await session.commit()
    return {'status': 'OK'} 


@router.patch("/{task_id}")
async def edit_task(
    task_id: int,
    task_data: PatchTask,
    creator: dict = Depends(is_head_role)
):
    async with async_session_maker() as session:
        query = select(TasksOrm).filter_by(id=task_id)
        result = await session.execute(query)
        task = result.scalars().one_or_none()
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        edit_stat = update(TasksOrm).filter_by(id = task_id).values(**task_data.model_dump(exclude_unset = True))
        await session.execute(edit_stat)
        await session.commit()
    return {'status': 'OK'}


@router.delete("/{task_id}")
async def  delete_task(
    task_id: int,
    creator: dict = Depends(is_head_role)
):
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
        task = res.scalars().one_or_none()
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        return task


@router.get("")
async def get_tasks(
    executor_email: str,
    current_user: dict = Depends(get_current_user) 
):
    if current_user["email"] != executor_email and current_user["role"] != "head":
        raise HTTPException(status_code=403, detail="Вы не можете просматривать чужие задачи")
    async with async_session_maker() as session:
        query = select(TasksOrm).filter_by(executor_email = executor_email)
        res = await session.execute(query)
    return res.scalars().all()




