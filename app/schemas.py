from pydantic import BaseModel, EmailStr

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

    class Config:
        orm_mode = True

# Para login
class UserLogin(BaseModel):
    email: EmailStr
    password: str
