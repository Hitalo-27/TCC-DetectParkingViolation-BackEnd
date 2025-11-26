from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from typing import List

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
        from_attributes = True

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

class AddressBase(BaseModel):
    pais: str
    estado: str
    cidade: str
    rua: str
    numero: Optional[int] = None
    longitude: str
    latitude: str

    class Config:
        from_attributes = True

class CarBase(BaseModel):
    cor: Optional[str] = None
    placa_numero: Optional[str] = None
    origem: str
    endereco_id: Optional[int] = None

    class Config:
        from_attributes = True

class TypeOfInfractionBase(BaseModel):
    gravidade: str
    pontos: int
    descricao: str

    class Config:
        from_attributes = True

class InfractionsBase(BaseModel):
    data: Optional[datetime] = None
    imagem: Optional[str] = None
    veiculo: CarBase
    endereco: Optional[AddressBase] = None
    tipo_infracao: TypeOfInfractionBase
    user: UserResponse

    class Config:
        from_attributes = True

class InfractionsResponse(BaseModel):
    placa: Optional[str] = None
    infracoes: List[InfractionsBase]

    class Config:
        from_attributes = True

class NotificationCreate(BaseModel):
    mensagem: str
    data: datetime
    user_id: int

class NotificationBase(BaseModel):
    mensagem: str
    data: datetime
    user: UserResponse

    class Config:
        from_attributes = True