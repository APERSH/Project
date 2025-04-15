from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func

from datetime import datetime

from src.database import Base

class TaskEvaluationOrm(Base):
    __tablename__ = "taskevaluations"

    id: Mapped[int] = mapped_column(primary_key = True)
    task_id: Mapped[int] = mapped_column(nullable=False)
    evaluator_id: Mapped[int] = mapped_column(nullable=False)
    executor_id: Mapped[int] = mapped_column(nullable=False)
    timeliness: Mapped[int] = mapped_column(nullable=False)
    quality: Mapped[int] = mapped_column(nullable=False) 
    completeness: Mapped[int] = mapped_column(nullable=False) 
    comment: Mapped[str] = mapped_column(nullable=True)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default = func.now()) 