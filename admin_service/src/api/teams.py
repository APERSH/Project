from fastapi import APIRouter, HTTPException


from schemas.teams import Team
from database import async_session_maker
from sqlalchemy import insert, select, update
from models.teams import TeamsOrm

router = APIRouter(prefix="/teams", tags=["Администрирование команд"])

   

@router.post("/register")
async def register_team(
    data: Team
):
    async with async_session_maker() as session:
        add_stat = insert(TeamsOrm).values(**data.model_dump(exclude_unset=True))
        await session.execute(add_stat)
        await session.commit() 
    return {'status': 'OK'} 


@router.get("/{team_id}")
async def get_one_team(team_id: int):
    async with async_session_maker() as session:
        query = select(TeamsOrm).filter_by(id=team_id)
        res = await session.execute(query)
        team =  res.scalars().one_or_none()
        if team is None:
            raise HTTPException(status_code=404, detail="Команда не найдена")
        return team
    
@router.put("/{team_id}")
async def edit_team(
    team_id: int,
    data: Team
):
    async with async_session_maker() as session:
        edit_stat = (
            update(TeamsOrm)
            .filter_by(id=team_id)
            .values(**data.model_dump(exclude_unset=True))
            .returning(TeamsOrm.id)
        )
        result = await session.execute(edit_stat)
        updated = result.scalars().one_or_none()
        if updated is None:
            raise HTTPException(status_code=404, detail="Команда не найдена")
        await session.commit() 
    return {'status': 'OK'}