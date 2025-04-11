from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime

from datetime import datetime

from src.database import Base

class CalendarOrm(Base):
    __tablename__ = "calendars"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    meeting_id: Mapped[int] = mapped_column(nullable=False)
    user_email: Mapped[str] = mapped_column(nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)