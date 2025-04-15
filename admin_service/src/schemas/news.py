from pydantic import BaseModel


class News(BaseModel):
    title : str
    content: str
    team_id: int
    department_id: int