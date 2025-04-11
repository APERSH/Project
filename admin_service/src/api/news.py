from fastapi import APIRouter

from models.news import NewsOrm
from schemas.news import News
from database import async_session_maker
from sqlalchemy import insert, select

router = APIRouter(prefix="/news", tags=["Новости"])

@router.post("/register")
async def register_news(
    data_news: News
):
    async with async_session_maker() as session:
        add_stat = insert(NewsOrm).values(**data_news.model_dump())
        await session.execute(add_stat)
        await session.commit() 
    return {'status': 'OK'}


@router.get("")
async def get_all_news():
    async with async_session_maker() as session:
        add_stat = select(NewsOrm)
        res = await session.execute(add_stat)
    return res.scalars().all()

@router.get("/{news_id}")
async def get_news(
    news_id: int
):
    async with async_session_maker() as session:
        add_stat = select(NewsOrm).filter_by(id = news_id)
        res = await session.execute(add_stat)
    return res.scalars().one_or_none()
