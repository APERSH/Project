from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class DepartmentsOrm(Base):
    __tablename__ = "departments"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(nullable=False, unique = True)
    team_id : Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete = "CASCADE"))
    head_user_email: Mapped[str | None] = mapped_column(None, nullable = True)