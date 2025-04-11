from pydantic import BaseModel

from datetime import datetime


class TaskEvaluationAdd(BaseModel):
    task_id: int
    evaluator_id: int
    executor_id: int
    timeliness: int
    quality: int
    completeness: int
    comment: str 
    created_at: datetime