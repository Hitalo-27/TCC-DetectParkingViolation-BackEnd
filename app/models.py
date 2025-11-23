from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    image_url = Column(String, nullable=True)

class Address(Base):
    __tablename__ = "endereco"

    id = Column(Integer, primary_key=True, index=True)
    pais = Column(String(45), index=True, nullable=False)
    estado = Column(String(80), index=True, nullable=False)
    cidade = Column(String(80), index=True, nullable=False)
    rua = Column(String(100), nullable=False)
    numero = Column(Integer, nullable=True)
    longitude = Column(String(50), nullable=False)
    latitude = Column(String(50), nullable=False)

    veiculos = relationship("Car", back_populates="endereco")

class Car(Base):
    __tablename__ = "veiculo"

    id = Column(Integer, primary_key=True, index=True)
    cor = Column(String(30), index=True, nullable=False)
    placa_numero = Column(String(7), index=True, nullable=False)
    origem = Column(String(45), index=True, nullable=False)

    endereco_id = Column(Integer, ForeignKey("endereco.id"), nullable=False)

    endereco = relationship("Address", back_populates="veiculos")

class TypeOfInfraction(Base):
    __tablename__ = "tipo_infracao"

    id = Column(Integer, primary_key=True, index=True)
    gravidade = Column(String(100), index=True, nullable=False)
    pontos = Column(Integer, nullable=False)
    descricao = Column(String(255), nullable=False)

class Infraction(Base):
    __tablename__ = "infracoes"
    id = Column(Integer, primary_key=True)
    data = Column(DateTime)
    imagem = Column(String, nullable=True)

    veiculo_id = Column(Integer, ForeignKey("veiculo.id"))
    veiculo = relationship("Car")  # agora veiculo é o objeto completo

    endereco_id = Column(Integer, ForeignKey("endereco.id"))
    endereco = relationship("Address")  # objeto completo

    tipo_infracao_id = Column(Integer, ForeignKey("tipo_infracao.id"))
    tipo_infracao = relationship("TypeOfInfraction")  # objeto completo

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")  # objeto completo