from fastapi import APIRouter, Depends
from pathlib import Path
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..database import get_db
from functools import partial
from .. import models
from app.controllers.detect_infractions_controller import detect_infractions
from app.utils.get_plate_api import get_plate
import asyncio

router = APIRouter(prefix="/validations", tags=["Validation"])

APP_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = APP_DIR.parent
video_path = BASE_DIR / "video" / "Car4.mp4"
model_path = APP_DIR / "models" / "prototipo_1.pt"
image_path = APP_DIR / "images" / "carro_teste.png"

@router.post("/validation-video")
async def validation_video():
    if not model_path.exists():
        return {"error": f"Modelo não encontrado em: {model_path}"}
    if not video_path.exists():
        return {"error": f"Vídeo não encontrado em: {video_path}"}

    loop = asyncio.get_event_loop()
    
    func_call = partial(
        detect_infractions, 
        model_path=str(model_path), 
        image_path=None, 
        video_path=str(video_path)
    )
    
    saved_file_path = await loop.run_in_executor(None, func_call)
    
    return {
        "status": "Processo de vídeo concluído",
        "output_file": saved_file_path
    }

@router.post("/validation-image")
async def validation_image(db: Session = Depends(get_db)):
    new_cars = []

    try:
        if not model_path.exists():
            return {"error": f"Modelo não encontrado em: {model_path}"}
        if not image_path.exists():
            return {"error": f"Imagem não encontrada em: {image_path}"}

        loop = asyncio.get_event_loop()
        func_call = partial(
            detect_infractions,
            model_path=str(model_path),
            image_path=str(image_path),
            video_path=None
        )

        detect_result = await loop.run_in_executor(None, func_call)


        for key in detect_result["detections"]:
            # car_address = get_plate(key["license_plate"])

            new_car = models.Car(
                cor=key["color"],
                placa_numero=key["license_plate"],
                origem="teste",
                endereco_id=1 
            )
            db.add(new_car)
            new_cars.append(new_car)

        db.commit()

        for car in new_cars:
            db.refresh(car)

        return {
            "status": "Processo de imagem concluído",
            "result": detect_result
        }
    
    except Exception as e:
        db.rollback() 
        print(f"Erro ao salvar no banco: {e}")

        raise HTTPException(
            status_code=500,  
            detail=f"Erro ao salvar no banco: {str(e)}"
        )
    
@router.post("/teste")
async def validation_image(db: Session = Depends(get_db)):
    image_path = APP_DIR / "images" / "carro_teste.png"