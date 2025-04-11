from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import settings
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(url = settings.DB_URL)
async_session_maker = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass