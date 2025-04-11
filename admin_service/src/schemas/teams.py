from pydantic import BaseModel


class Team(BaseModel):
    name: str
    description: str
    invite_code: str | None = None