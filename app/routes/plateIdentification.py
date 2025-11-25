from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from .. import schemas, models, auth
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
from app.routes.infracoes import validar_infracao
from datetime import datetime

UPLOAD_DIR = "app/uploads"
UPLOAD_DIR_RELATIVE = "uploads"

router = APIRouter(prefix="/plate", tags=["veiculos"])

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_KEY")
GEMINI_URL = os.getenv("GEMINI_URL")

# Body -> Multipart -> file = imagem
@router.post("/identification")
async def get_plate(db: Session = Depends(get_db), file: UploadFile = File(...), current_email: str = Depends(auth.get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_email).first()

    try:
        isInfraction = await validar_infracao(file)
        
        car_deatils = isInfraction.get("carro")
        
        if car_deatils == []:
            return {
                "response": "Sem carro identificado"
            }
        # Quando detecta um carro
        if car_deatils.get("tem_infracao"):
            
            # Buscando a infração
            infraction_type = db.query(models.TypeOfInfraction).filter(models.TypeOfInfraction.descricao == car_deatils.get("infractions", [{}])[0].get("tipo")).first()
        
            try:
                # Resetando o file porquê se não dar erro na leitura da função (depois passar o file já lido)
                await file.seek(0)
                # Pegando a placa
                placa = await get_plate_function(file)
                
                print("EPA 2")
                car_information = chamando(placa)
                # Caso encontre as informações do carro através da placa
                if car_information.get('error'):
                    color_car = 'Não encontrado'
                    car_estado = "Não identificado"
                    car_cidade = "Não identificado"            
                    
                else:
                    color_car = car_information['veiculos']['cd_cor_veiculo']
                    car_estado = car_information['veiculos']['sg_uf']
                    car_cidade = car_information['veiculos']['cd_municipio'].strip()
                    
                car_address = models.Address(
                    pais="Brasil",
                    estado=car_estado,
                    cidade=car_cidade
                )    
                
                db.add(car_address)

                db.commit()

                db.refresh(car_address)

                address_id = car_address.id
                
                new_car = models.Car(
                    cor=color_car,
                    placa_numero=placa,
                    origem="teste",
                    endereco_id=address_id
                )
                        
                db.add(new_car)
                db.commit()
                db.refresh(new_car)
                
                new_car.id
                
                # Chamadando a função que pega a localização a partir dos metadados
                local = await extract_image_metadata(file)
                print("EPA 3 ", local)
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
                    
                else:
                    infraction_local_street = 'Não localizado'
                    infraction_local_number = 0
                    
                    new_address_infraction = models.Address(
                        pais="Brasil",
                        estado=infraction_local_street,
                        cidade=infraction_local_street,
                        rua=infraction_local_street,
                        numero=infraction_local_number,
                        longitude=0,
                        latitude=0
                    )

                    
                db.add(new_address_infraction)
                db.commit()
                db.refresh(new_address_infraction)                    
                    
                date_now = datetime.now()
                date_formated = date_now.strftime("%Y-%m-%d %H:%M")
                
                infraction = models.Infraction(
                    imagem='/uploads/' + file.filename,
                    data=date_now,
                    veiculo_id=new_car.id,
                    endereco_id=new_address_infraction.id,
                    tipo_infracao_id=infraction_type.id,
                    user_id=user.id
                )

                db.add(infraction)
                db.commit()
                db.refresh(infraction) 
                print("EPA 4")
                # Fazer um try catch decente
                return {
                    "hasInfraction": True,
                    "plate": placa,
                    "location": infraction_local_street + ', ' + str(infraction_local_number),
                    "datetime": date_formated,
                    "infraction": car_deatils.get("infractions", [{}])[0].get("tipo"),
                    "type": infraction_type.gravidade,
                }                                                  
            except Exception as e:
                return {
                    "response": "Erro na hora de identificar a infração",
                    "erro": str(e)
                }
        else:
            # detectou o carro mas não tinha nenhuma infração
            return {
                "response": "Sem infração identificada"
            }
    except Exception as e:
        return {
            "response": "Foi de base",
            "erro": str(e)
        }