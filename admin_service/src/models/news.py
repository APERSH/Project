from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Text


class NewsOrm(Base):
    __tablename__ = "news"

    id : Mapped[int] = mapped_column(primary_key=True)
    title : Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete = "CASCADE"))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id", ondelete = "CASCADE"))