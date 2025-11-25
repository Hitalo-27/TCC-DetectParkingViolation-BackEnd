from fastapi import APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from app.platereq import dadosveiculo

UPLOAD_DIR = "app/uploads"
UPLOAD_DIR_RELATIVE = "uploads"

router = APIRouter(prefix="/veiculos", tags=["veiculos"])

@router.get("/reqteste")
def reqteste(placa: str = "IMN4068"):
    """
    Ex.: acessar http://localhost:8000/reqteste?placa=IMN4068
    """
    resultado = dadosveiculo(placa)
    # Retorna diretamente o JSON vindo da API externa
    return {"message": "placa consultada", "dados": resultado}