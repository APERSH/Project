from fastapi import APIRouter,Request, HTTPException
from fastapi.encoders import jsonable_encoder
import httpx

from schemas.meetings import Meeting, AddMeeting, AddParticipant, Participant, AddEvents
from database import async_session_maker
from sqlalchemy import insert, select, update, delete
from models.meetings import MeetingOrm, MeetingParticipantOrm


router = APIRouter(prefix="/meetings", tags=["Встречи"])

@router.post("/register")
async def create_meeting(
    meeting_data: AddMeeting,
    request: Request
):
    async with httpx.AsyncClient(cookies=request.cookies) as session:
        res = await session.get(f"http://localhost:8000/users")
        current_user = res.json()
    new_meeting_data = Meeting(
        team_name = current_user["team_name"],
        department_name = current_user["department_name"],
        title = meeting_data.title,
        start_time = meeting_data.start_time,
        end_time = meeting_data.end_time,
        creator_id = current_user["id"]
    )
    async with async_session_maker() as session:
        add_stat = insert(MeetingOrm).values(**new_meeting_data.model_dump())
        await session.execute(add_stat)
        await session.commit()
    return {'status': 'OK'} 


@router.put("/{meeting_id}")
async def edit_meeting(
    meeting_id: int,
    meeting_data: AddMeeting,
    request: Request
):
    async with httpx.AsyncClient(cookies=request.cookies) as session:
        res = await session.get(f"http://localhost:8000/users")
        current_user = res.json()
    async with async_session_maker() as session:
        query = select(MeetingOrm).filter_by(id = meeting_id)
        res = await session.execute(query)
        meeting = res.scalars().one_or_none()
    if not current_user["id"] == meeting.creator_id:
        raise HTTPException(status_code = 403, detail="Вы не создатель встречи")
    async with async_session_maker() as session:
        edit_stat = update(MeetingOrm).filter_by(id = meeting_id).values(**meeting_data.model_dump())
        await session.execute(edit_stat)
        await session.commit()
    return {'status': 'OK'}

@router.delete("/{meeting_id}")
async def delete_meeting(
    meeting_id: int,
    request: Request
):
    async with httpx.AsyncClient(cookies=request.cookies) as session:
        res = await session.get(f"http://localhost:8000/users")
        current_user = res.json()
    async with async_session_maker() as session:
        query = select(MeetingOrm).filter_by(id = meeting_id)
        res = await session.execute(query)
        meeting = res.scalars().one_or_none()
    if not current_user["id"] == meeting.creator_id:
        raise HTTPException(status_code = 403, detail="Вы не создатель встречи")
    async with async_session_maker() as session:
        del_stat = delete(MeetingOrm).filter_by(id = meeting_id)
        await session.execute(del_stat)
        await session.commit()
    return {'status': 'OK'}


@router.post("/add/{user_email}")
async def add_participant(
    user_email: str,
    request: Request,
    participant_data: AddParticipant
):
    async with httpx.AsyncClient(cookies=request.cookies) as session:
        res = await session.get(f"http://localhost:8000/users/{user_email}")
        user = res.json()
    async with async_session_maker() as session:
        query = select(MeetingOrm).filter_by(id = participant_data.meeting_id)
        meeting_res = await session.execute(query)
        meeting = meeting_res.scalars().one_or_none()
    if  not user["team_name"] == meeting.team_name and not user["department_name"] == meeting.department_name:
        raise HTTPException(status_code = 403, detail="Access denied")
    async with async_session_maker() as session:
        query = select(MeetingParticipantOrm).filter_by(meeting_id = participant_data.meeting_id, user_id = user["id"])
        participant_res = await session.execute(query)
        participant = participant_res.scalars().one_or_none()
    if participant:
        raise HTTPException(status_code = 400, detail="Пользователь уже добавлен")
    async with httpx.AsyncClient() as session:
        events = await session.get(f"http://localhost:8005/calendar/{user['email']}/{meeting.start_time.replace(tzinfo=None, microsecond=0)}/{meeting.end_time.replace(tzinfo=None, microsecond=0)}")
        event = events.json()
    if event:
        raise HTTPException(status_code = 400, detail="Пользователь занят")
    new_participant_data = Participant(
        meeting_id = participant_data.meeting_id,
        user_id = user["id"]
    )
    new_events_data = AddEvents(
        title = meeting.title,
        meeting_id = meeting.id,
        user_email = user["email"],
        start_time = meeting.start_time.isoformat(),
        end_time = meeting.end_time.isoformat()
    )
    data = jsonable_encoder(new_events_data)
    async with async_session_maker() as session:
        add_stat = insert(MeetingParticipantOrm).values(**new_participant_data.model_dump())
        await session.execute(add_stat)
        await session.commit()
    async with httpx.AsyncClient() as session:
        await session.post(f"http://localhost:8005/calendar/register", json = data)
    return {'status': 'OK'}
    
    