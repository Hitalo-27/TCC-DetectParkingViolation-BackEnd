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
from app.utils.convert_to_decimal import dms_to_decimal
from ..database import get_db
from app.routes.imageIdentification import extract_image_metadata
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
    # Chamar primeiramente a função que valida a infração, se não houver, nem precisa executar o resto da rota
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
        
        # Chamadando a função que pega a localização a partir dos metadados
        local = await extract_image_metadata(file)
        
        if local.get('local'):
            # Criando o endereço que vai ser relacionado com a infração (local onde ocorreu a infração)    
            infraction_local_street = local['local']['rua']
            infraction_local_number = local['local']['numero']
            
            # Função para converter a latidude e longitude para o padrão que esperamos -**,****
            latitude = dms_to_decimal(local['metadados']['GPSInfo']['GPSLatitude'], local['metadados']['GPSInfo']['GPSLatitudeRef'])
            longitude = dms_to_decimal(local['metadados']['GPSInfo']['GPSLongitude'], local['metadados']['GPSInfo']['GPSLongitudeRef'])
            
            new_address_infraction = models.Address(
                pais="Brasil",
                estado=local['local']['estado'],
                cidade=local['local']['cidade'],
                rua=infraction_local_street,
                numero=infraction_local_number,
                longitude=longitude,
                latitude=latitude
            )
            
            db.add(new_address_infraction)
            db.commit()
            db.refresh(new_address_infraction)
        else:
            infraction_local_street = 'Não localizado'
            infraction_local_number = 'Não localizado'
        
        print(f"Response: {new_car}")
        
        date_now = datetime.now()
        date_formated = date_now.strftime("%Y-%m-%d %H:%M")

        # Fazer um try catch decente
        return {
            "hasInfraction": True,
            "plate": placa,
            "location": infraction_local_street + ', ' + infraction_local_number,
            "datetime": date_formated,
            "infraction": "Estacionamento em vaga de idoso sem credencial",
            "type": "Grave",
        }
    except httpx.HTTPStatusError as e:
        db.rollback()
        raise
