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

class CarBase(BaseModel):
    cor: str
    placa_numero: str
    origem: str
    endereco_id: int

class TypeOfInfractionBase(BaseModel):
    gravidade: str
    pontos: int
    descricao: str

class InfractionsBase(BaseModel):
    data: datetime
    imagem: Optional[str] = None
    veiculo: CarBase
    endereco: AddressBase
    tipo_infracao: TypeOfInfractionBase
    arquivo: Optional[int] = None

class InfractionsResponse(BaseModel):
    placa: str
    infracoes: List[InfractionsBase]