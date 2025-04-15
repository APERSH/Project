from pydantic import BaseModel

from datetime import datetime

class Meeting(BaseModel):
    team_name: str
    department_name: str
    title: str
    start_time: datetime
    end_time: datetime
    creator_id: int

class AddMeeting(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime
    
class AddParticipant(BaseModel):
    meeting_id: int


class Participant(BaseModel):
    meeting_id: int
    user_id: int

class AddEvents(BaseModel):
    title: str
    meeting_id: int
    user_email: str
    start_time: datetime
    end_time: datetime
    