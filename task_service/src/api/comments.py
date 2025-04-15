from fastapi import APIRouter
from sqlalchemy import insert

from schemas.comments import CreateComment
from database import async_session_maker
from models.tasks import TaskCommentsOrm

router = APIRouter(prefix="/comments", tags=["Добавление комментариев"])


@router.post("/")
async def add_comment(
    comment_data: CreateComment
):
    async with async_session_maker() as session:
        add_stat = insert(TaskCommentsOrm).values(**comment_data.model_dump())
        await session.execute(add_stat)
        await session.commit()
    return {'status': 'OK'}