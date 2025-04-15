
from fastapi import APIRouter, HTTPException
from sqlalchemy import select, insert

from datetime import datetime, timedelta, timezone
import calendar

from database import async_session_maker
from models.calendar import CalendarOrm
from schemas.events import Event


router = APIRouter(prefix="/calendar", tags=["Календарь событий"])

@router.get("/{user_id}/day")
async def get_events_of_day(
    user_id: int
):
    now = datetime.now(timezone.utc)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    async with async_session_maker() as session:
        query = select(CalendarOrm).filter(CalendarOrm.user_id == user_id, 
                                           CalendarOrm.start_time < end_of_day,
                                           CalendarOrm.end_time >= start_of_day)
        res = await session.execute(query)
        return res.scalars().all()
    

@router.get("/{user_id}/month")
async def get_events_of_month(
    user_id: int
):
    now = datetime.now(timezone.utc)
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    year = start_of_month.year
    month = start_of_month.month
    last_day = calendar.monthrange(year, month)[1]
    end_of_month = start_of_month.replace(day=last_day) + timedelta(days=1)
    async with async_session_maker() as session:
        query = select(CalendarOrm).filter(CalendarOrm.user_id == user_id, 
                                              CalendarOrm.start_time < end_of_month,
                                              CalendarOrm.end_time > start_of_month)
        res = await session.execute(query)
        return res.scalars().all()
    

@router.get("/{user_id}/{start_meeting}/{end_meeting}")
async def get_events_by_time(
    start_meeting: datetime,
    end_meeting: datetime,
    user_id: id 
):
    async with async_session_maker() as session:
        query = select(CalendarOrm).filter(CalendarOrm.user_id == user_id,
                                           CalendarOrm.start_time <= end_meeting,
                                            CalendarOrm.end_time >= start_meeting)
        res = await session.execute(query)
        return res.scalars().all()
    
@router.post("/register")
async def create_events(
    events_data: Event
):
    async with async_session_maker() as session:
        check_query = select(CalendarOrm).filter_by(
            title=events_data.title,
            meeting_id=events_data.meeting_id,
            start_time=events_data.start_time,
            end_time=events_data.end_time
        )
        existing = await session.execute(check_query)
        if existing.scalars().one_or_none():
            raise HTTPException(status_code=409, detail="Событие уже существует")
        add_stat = insert(CalendarOrm).values(**events_data.model_dump(exclude_unset=True)).returning(CalendarOrm.title)
        result = await session.execute(add_stat)
        title = result.scalar_one()
        await session.commit()
    return {'status': 'OK', "title": title}