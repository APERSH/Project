from pydantic import BaseModel, Field

class Department(BaseModel):
    name : str
    team_id : int
    head_user_email: str 

class DepratmentPatch(BaseModel):
    name : str | None = Field(None)
    team_id : int | None = Field(None)
    head_user_email: str | None = Field(None)