from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from .. import schemas, models
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
import base64
import httpx
from app.platereq import chamando
from app.utils.get_plate_api import get_plate_function
from ..database import get_db
from datetime import datetime

UPLOAD_DIR = "app/uploads"
UPLOAD_DIR_RELATIVE = "uploads"

router = APIRouter(prefix="/plate", tags=["veiculos"])

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_KEY")
GEMINI_URL = os.getenv("GEMINI_URL")

# Body -> Multipart -> file = imagem
@router.post("/identification")
async def get_plate(db: Session = Depends(get_db), file: UploadFile = File(...)):
    # return {
    #     "hasInfraction": True,
    #     "plate": "placa",
    #     "location": "Rua Oscar Freire, 123",
    #     "datetime": "date_formated",
    #     "infraction": "Estacionamento em vaga de idoso sem credencial",
    #     "type": "Grave",
    # }
    
    try:
        placa = await get_plate_function(file)

        print(f"Response: {placa}")   
        
        car_information = chamando(placa)

        print(car_information)
        
        
        if car_information.get('error'):
            print("EBA")
            color_car = 'Não encontrado'
            car_estado = "Não identificado"
            car_cidade = "Não identificado"            
            
        else:
            print("Não")
            color_car = car_information['veiculos']['cd_cor_veiculo']
            car_estado = car_information['veiculos']['sg_uf']
            car_cidade = car_information['veiculos']['cd_municipio'].strip()
            
            
        new_address = models.Address(
            pais="Brasil",
            estado=car_estado,
            cidade=car_cidade
        )    
        
        db.add(new_address)

        db.commit()

        db.refresh(new_address)

        address_id = new_address.id
        
        new_car = models.Car(
            cor=color_car,
            placa_numero=placa,
            origem="teste",
            endereco_id=address_id
        )
                
        db.add(new_car)
        db.commit()
        db.refresh(new_car)
        
        print(f"Response: {new_car}")
        
        date_now = datetime.now()
        date_formated = date_now.strftime("%Y-%m-%d %H:%M")

        # Chamar função que verifica infração
        # chamar api que pega os metadados
        # Fazer um try catch decente
        return {
            "hasInfraction": True,
            "plate": placa,
            "location": "Rua Oscar Freire, 123",
            "datetime": date_formated,
            "infraction": "Estacionamento em vaga de idoso sem credencial",
            "type": "Grave",
        }
    except httpx.HTTPStatusError as e:
        db.rollback()
        raise
    #         return JSONResponse(
    #             status_code=e.response.status_code, 
    #             content={"erro": "Falha ao processar imagem", "error => ": e.response.json()}
    #         )
    # except httpx.RequestError as e:
    #         # Erro de rede (ex: timeout, não conseguiu conectar)
    #     print(f"Falha ao processar imagem, servidor não respondeu: {e}")
    #     return JSONResponse(
    #         status_code=503, # Service Unavailable
    #         content={"erro": "Não foi possível conectar ao serviço", "error => ": str(e)}
    #     )
    # except Exception as e:
    #     # Erro genérico (ex: falha ao ler o arquivo, falha no base64, etc)
    #     print(f"Erro inesperado: {e}")
    #     return JSONResponse(status_code=500, content={"erro": "Erro interno no servidor", "error => ": str(e)})    
