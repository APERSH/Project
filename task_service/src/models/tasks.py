from sqlalchemy import Text, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SQLEnum

from enum import Enum
from datetime import datetime

from src.database import Base

class TaskStatus(Enum):
    open = "Открыто"
    in_progress = "В работе"
    completed = "Выполнено"


class TasksOrm(Base):
    __tablename__ = "tasks"

    id : Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus), default=TaskStatus.open)
    creator_email: Mapped[str] = mapped_column(nullable=False)
    executor_email: Mapped[str] = mapped_column(nullable=False)
    created_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default = func.now())
    updated_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class TaskCommentsOrm(Base):
    __tablename__ = "task_comments"

    id : Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    author_email: Mapped[str] = mapped_column(nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    created_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default = func.now())