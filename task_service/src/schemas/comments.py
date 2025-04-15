from pydantic import BaseModel
from datetime import datetime

class CreateComment(BaseModel):
    task_id: int
    author_email: str
    comment: str
    created_on: datetime