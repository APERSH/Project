from fastapi import APIRouter, Request, HTTPException
import httpx
from sqlalchemy import insert, select

from schemas.evaluations import TaskEvaluationAdd
from database import async_session_maker
from models.evaluation import TaskEvaluationOrm




router = APIRouter(prefix="/evaluations", tags=["Оценивание"])

@router.post("/register")
async def register_evaluation(
    request: Request,
    ev_data: TaskEvaluationAdd,
):
    async with httpx.AsyncClient(cookies=request.cookies) as session:
        creator_resp = await session.get(f"http://localhost:8000/users") 
        current_user =  creator_resp.json()
        resp = await session.get(f"http://localhost:8002/tasks/{ev_data.task_id}")
        task = resp.json()
    if not current_user["email"] == task["creator_email"]:
        raise HTTPException(status_code=403, detail="Вы не можете оценивать выполнение")
    async with async_session_maker() as session:
        add_stat = insert(TaskEvaluationOrm).values(**ev_data.model_dump())
        await session.execute(add_stat)
        await session.commit()
    return {'status': 'OK'} 


@router.get("/{task_id}")
async def get_evaluations_by_task_id(
    task_id:int
):
    async with async_session_maker() as session:
        query = select(TaskEvaluationOrm).filter_by(task_id = task_id)
        res = await session.execute(query)
        evalation = res.scalars().one_or_none()
    return evalation


@router.get("/users/{user_id}")
async def get_evaluations_by_task_id(
    user_id:int
):
    async with async_session_maker() as session:
        query = select(TaskEvaluationOrm).filter_by(executor_id = user_id)
        res = await session.execute(query)
        evalations = res.scalars().all()
    avg = lambda field: sum(getattr(ev, field) for ev in evalations) / len(evalations)
    return {
    "timeliness": avg("timeliness"),
    "quality": avg("quality"),
    "completeness": avg("completeness")
}