from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    name: str 
    email: EmailStr
    password : str = Field(min_length=6)
    team_name : str
    department_name: str

class LoginUser(BaseModel):
    email: EmailStr
    password : str = Field(min_length=6)


class PatchUser(BaseModel):
    name: str| None = None
    email: EmailStr| None = None
    password : str| None = Field(None, min_length=6)
    team_name : str| None = None
    access_level: str| None = None
    role: str| None = None
    department_name: str| None = None





