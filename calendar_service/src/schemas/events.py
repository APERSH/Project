from pydantic import BaseModel

from datetime import datetime

class Event(BaseModel):
    title: str
    meeting_id: int
    user_email: str
    start_time: datetime
    end_time: datetime