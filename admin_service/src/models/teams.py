from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text

class TeamsOrm(Base):
    __tablename__ = "teams"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(nullable=False, unique = True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    invite_code: Mapped[str] = mapped_column(nullable=True)