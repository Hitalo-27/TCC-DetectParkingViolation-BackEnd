from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from pathlib import Path
import base64
import httpx
from sqlalchemy.orm import Session
from ..database import get_db
from app.controllers.detect_infractions_controller import detect_infractions

router = APIRouter(prefix="/validations", tags=["Validation"])

@router.post("/validation-image")
async def validation_image(db: Session = Depends(get_db), file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        
        # Convertendo a imagem em BASE64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # Chamar função que valida a infração
        # Se sim:
        
    except httpx.HTTPStatusError as e:
        
        return JSONResponse(
            status_code=e.response.status_code, 
            content={"erro": "Falha ao processar imagem", "error => ": e.response.json()}
        )
    
@router.post("/teste")
async def validation_image(db: Session = Depends(get_db)):
    image_path = APP_DIR / "images" / "carro_teste.png"