from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    is_active: bool = True

class User(UserCreate):
    id: int
    name: str
    email: str
    is_active: bool

    class Config:
        orm_mode = True