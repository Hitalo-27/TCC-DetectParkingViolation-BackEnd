from fastapi import APIRouter, Depends, HTTPException, Body, File, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .. import schemas, models, auth
from ..database import get_db
import os
import cv2
from ultralytics import YOLO
from app.controllers.validarinfracoes import validar_infracao as validar_infracao_raw
import numpy as np

MODEL_PATH = "app/models/best.pt"
UPLOAD_DIR = "app/uploads"

model = YOLO(MODEL_PATH)

router = APIRouter(prefix="/infracoes", tags=["infracoes"])


@router.get("/consultar", response_model=schemas.InfractionsResponse)
def consultar_infracoes(
    placa: str = None,
    user: int = None,
    db: Session = Depends(get_db),
    current_email: str = Depends(auth.get_current_user)
):
    if placa:
        veiculo = db.query(models.Car).filter(models.Car.placa_numero == placa).first()
        if not veiculo:
            raise HTTPException(status_code=404, detail="Nenhuma infração encontrada para esta placa")
        infracoes = db.query(models.Infraction).filter(models.Infraction.veiculo_id == veiculo.id).all()
        if not infracoes:
            raise HTTPException(status_code=404, detail="Nenhuma infração encontrada para esta placa")
        return {"placa": veiculo.placa_numero, "infracoes": infracoes}

    if user:
        infracoes = db.query(models.Infraction).filter(models.Infraction.user_id == user).all()
        if not infracoes:
            raise HTTPException(status_code=404, detail="Nenhuma infração encontrada para este usuário")
        return {"infracoes": infracoes}


@router.post("/validar")
async def validar_infracao_endpoint(
    # data: dict = Body(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_email: str = Depends(auth.get_current_user)
):
    
    try:
        # filename = data.get("filename")
        # if not filename:
        #     return JSONResponse(
        #         status_code=400,
        #         content={"erro": "Campo 'filename' é obrigatório no corpo da requisição."},
        #     )

        # image_path = os.path.join(UPLOAD_DIR, filename)
        # if not os.path.exists(image_path):
        #     return JSONResponse(
        #         status_code=404,
        #         content={"erro": f"Arquivo '{filename}' não encontrado em {UPLOAD_DIR}"},
        #     )
        image_bytes = await file.read()
        np_arr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        # frame = cv2.imread(file)
        
        if frame is None:
            return JSONResponse(
                status_code=400,
                content={"erro": "Não foi possível abrir a imagem. Arquivo pode estar corrompido."},
            )

        resultado = validar_infracao_raw(frame, model, 'teste.png')

        return resultado

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"erro": "Erro ao processar imagem", "detalhes": str(e)},
        )
        
async def validar_infracao(file: UploadFile):
    try:
        image_bytes = await file.read()
        np_arr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return JSONResponse(
                status_code=400,
                content={"erro": "Não foi possível abrir a imagem. Arquivo pode estar corrompido."},
            )

        resultado = validar_infracao_raw(frame, model, 'teste.png')

        return resultado

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"erro": "Erro ao processar imagem", "detalhes": str(e)},
        )    