from pydantic import BaseModel, ConfigDict
from datetime import datetime
from models.tasks import TaskStatus

class CreateTask(BaseModel):
    title: str 
    description: str
    deadline: datetime
    status: TaskStatus
    creator_email: str
    executor_email: str
    created_on: datetime
    updated_on: datetime

    model_config = ConfigDict(from_attributes = True)


class PatchTask(BaseModel):
    description: str | None = None
    deadline: datetime | None = None
    status: TaskStatus | None = None
    

    model_config = ConfigDict(from_attributes = True)