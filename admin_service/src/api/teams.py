from fastapi import APIRouter


from schemas.teams import Team
from database import async_session_maker
from sqlalchemy import insert, select, update
from models.teams import TeamsOrm

router = APIRouter(prefix="/teams", tags=["Администрирование команд"])

   

@router.post("/register")
async def register_teams(
    data: Team
):
    new_team = Team(
        name = data.name, 
        description = data.description,
        invite_code = data.invite_code
    )
    async with async_session_maker() as session:
        add_stat = insert(TeamsOrm).values(**new_team.model_dump())
        await session.execute(add_stat)
        await session.commit() 
    return {'status': 'OK'} 


@router.get("/{team_id}")
async def get_one_team(team_id: int):
    async with async_session_maker() as session:
        query = select(TeamsOrm).filter_by(id = team_id)
        res = await session.execute(query)
        return res.scalars().one_or_none()
    
    
@router.put("/{team_id}")
async def edit_team(
    team_id: int,
    data: Team
):
    async with async_session_maker() as session:
        edit_stat = update(TeamsOrm).filter_by(id = team_id).values(**data.model_dump())
        await session.execute(edit_stat)
        await session.commit() 
    return {'status': 'OK'}