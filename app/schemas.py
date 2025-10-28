from pydantic import BaseModel, EmailStr
from typing import Optional

# Para entrada (cadastro)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Para resposta
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    image_url: Optional[str] = None

    class Config:
        orm_mode = True

# Para login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    old_password: Optional[str] = None
    new_password: Optional[str] = None
    new_password_confirm: Optional[str] = None