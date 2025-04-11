
from fastapi import APIRouter
from sqlalchemy import select, insert

from datetime import datetime, timedelta, timezone

from database import async_session_maker
from models.calendar import CalendarOrm
from schemas.events import Event


router = APIRouter(prefix="/calendar", tags=["Календарь событий"])

@router.get("/{user_email}/day")
async def get_events_of_day(
    user_email: str
):
    now = datetime.now(timezone.utc)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    async with async_session_maker() as session:
        query = select(CalendarOrm).filter(CalendarOrm.user_email == user_email, 
                                              CalendarOrm.end_time >= start_of_day,
                                              CalendarOrm.end_time < end_of_day)
        res = await session.execute(query)
        return res.scalars().all()
    

@router.get("/{user_email}/month")
async def get_events_of_month(
    user_email: str
):
    now = datetime.now(timezone.utc)
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if start_of_month.month == 12:
        next_month = start_of_month.replace(year=start_of_month.year + 1, month=1)
    else:
        next_month = start_of_month.replace(month=start_of_month.month + 1)
    async with async_session_maker() as session:
        query = select(CalendarOrm).filter(CalendarOrm.user_email == user_email, 
                                              CalendarOrm.end_time >= start_of_month,
                                              CalendarOrm.end_time < next_month)
        res = await session.execute(query)
        return res.scalars().all()
    

@router.get("/{user_email}/{start_meeting}/{end_meeting}")
async def get_events_by_time(
    start_meeting: datetime,
    end_meeting: datetime,
    user_email: str 
):
    async with async_session_maker() as session:
        query = select(CalendarOrm).filter(CalendarOrm.user_email == user_email,
                                           CalendarOrm.start_time <= end_meeting,
                                            CalendarOrm.end_time >= start_meeting)
        res = await session.execute(query)
        return res.scalars().all()
    
@router.post("/register")
async def create_events(
    events_data: Event
):
    async with async_session_maker() as session:
        add_stat = insert(CalendarOrm).values(**events_data.model_dump())
        await session.execute(add_stat)
        await session.commit()
    return {'status': 'OK'}