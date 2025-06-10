from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class TaskCreate(BaseModel):
    title: str
    user_id: int
