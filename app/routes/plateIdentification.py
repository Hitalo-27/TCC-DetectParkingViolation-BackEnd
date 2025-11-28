import uuid
from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder # Importação necessária para serializar o Pydantic
from ultralytics import YOLO
from sqlalchemy.orm import Session
from datetime import datetime
import os
import cv2
from dotenv import load_dotenv

# Importações internas
from .. import schemas, models, auth
from ..database import get_db
from app.platereq import dadosveiculo
from app.utils.get_plate_api import get_plate_function
from app.utils.convert_to_decimal import dms_to_decimal
from app.utils.imageIdentification import extract_image_metadata
from app.controllers.validarinfracoes import validar_infracao as validar_infracao_raw

# Configurações Iniciais
load_dotenv()
UPLOAD_DIR = "app/uploads"
MODEL_PATH = "app/models/best.pt"

# Inicialização do Modelo
model = YOLO(MODEL_PATH)
router = APIRouter(prefix="/plate", tags=["veiculos"])

# ---------------------------------------------------------
# FUNÇÕES AUXILIARES (HELPERS)
# ---------------------------------------------------------

def ensure_upload_dir_exists():
    """Garante que a pasta de uploads existe."""
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

async def save_uploaded_file(file: UploadFile) -> str:
    ensure_upload_dir_exists()
    
    original_name = file.filename
    _, ext = os.path.splitext(original_name)
    
    # Loop para garantir unicidade
    while True:
        random_name = f"{uuid.uuid4()}{ext}"
        saved_path = os.path.join(UPLOAD_DIR, random_name)
        
        # Se NÃO existir um arquivo com esse nome, sai do loop
        if not os.path.exists(saved_path):
            break

    # Salva o arquivo
    with open(saved_path, "wb") as f:
        f.write(await file.read())
        
    return saved_path

def get_or_create_vehicle(db: Session, placa: str, cor: str) -> models.Car:
    """
    Verifica se o carro já existe no banco.
    - Se existir: Retorna o objeto do carro existente.
    - Se NÃO existir: Consulta a API externa, cria o endereço do dono e o carro novo.
    """
    
    # 1. TENTA BUSCAR NO BANCO EXISTENTE
    existing_car = None

    if(placa != "Não Identificada"):
        existing_car = db.query(models.Car).filter(models.Car.placa_numero == placa).first()

    if existing_car:
        return existing_car

    # 2. SE NÃO EXISTE, BUSCA NA API E CRIA
    print(f"Carro {placa} não encontrado. Buscando dados na API externa...")
    car_info = dadosveiculo(placa)

    owner_address = None 

    color_car = cor  # Usa a cor identificada pela IA por padrão
    if car_info.get('veiculos'):
        # Caso de sucesso: extrai dados e CRIA endereço
        veic = car_info.get('veiculos', {})
        color_car = veic.get('cd_cor_veiculo', 'Desconhecida')
        car_estado = veic.get('sg_uf', 'BR')
        car_cidade = veic.get('cd_municipio', '').strip()
        
        # Cria e salva o endereço
        owner_address = models.Address(
            pais="Brasil",
            estado=car_estado,
            cidade=car_cidade
        )    
        db.add(owner_address)
        db.commit()
        db.refresh(owner_address)

    # Cria o novo carro
    new_car = models.Car(
        cor=color_car,
        placa_numero=placa,
        origem="API_Externa",
        endereco_id=owner_address.id if owner_address else None
    )
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    
    return new_car

def register_infraction_location_db(db: Session, metadata: dict) -> models.Address:
    """Registra o local onde a infração ocorreu."""
    local_info = metadata.get('local', {})
    gps_info = metadata.get('metadados', {}).get('GPSInfo', {})

    if local_info:
        rua = local_info.get('rua')
        numero = local_info.get('numero')
        estado = local_info.get('estado')
        cidade = local_info.get('cidade')
        
        lat = dms_to_decimal(gps_info.get('GPSLatitude'), gps_info.get('GPSLatitudeRef'))
        lon = dms_to_decimal(gps_info.get('GPSLongitude'), gps_info.get('GPSLongitudeRef'))
    else:
        rua = 'Não localizado'
        numero = 0
        estado = 'Não localizado'
        cidade = 'Não localizado'
        lat = 0
        lon = 0

    infraction_address = models.Address(
        pais="Brasil",
        estado=estado,
        cidade=cidade,
        rua=rua,
        numero=numero,
        longitude=lon,
        latitude=lat
    )
    db.add(infraction_address)
    db.commit()
    db.refresh(infraction_address)
    
    return infraction_address

def create_infraction_record(db: Session, image_path: str, car_id: int, address_id: int | None, type_id: int, user_id: int, data_infraction: str | None):
    """Cria o registro final da infração."""
    
    infraction = models.Infraction(
        imagem='/detect/' + image_path,
        data=data_infraction,
        veiculo_id=car_id,
        endereco_id=address_id,
        tipo_infracao_id=type_id,
        user_id=user_id
    )
    db.add(infraction)
    db.commit()
    db.refresh(infraction)
    return infraction

# ---------------------------------------------------------
# ROTA PRINCIPAL
# ---------------------------------------------------------

@router.post("/identification")
async def get_plate(
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    current_email: str = Depends(auth.get_current_user)
):
    try:
        # 1. Identificar Usuário
        user = db.query(models.User).filter(models.User.email == current_email).first()
        if not user:
            return JSONResponse(status_code=404, content={"success": False, "message": "Usuário não encontrado."})

        # 2. Salvar Imagem
        try:
            saved_path = await save_uploaded_file(file)
            filename = os.path.basename(saved_path)
        except Exception as e:
            return JSONResponse(status_code=500, content={"success": False, "message": f"Erro ao salvar arquivo: {str(e)}"})

        # 3. Carregar com OpenCV
        frame = cv2.imread(saved_path)
        if frame is None:
            return JSONResponse(status_code=400, content={"success": False, "message": "Imagem corrompida ou inválida."})

        # 4. Detecção de Infrações (YOLO)
        detection_result = validar_infracao_raw(frame, model, filename)
        car_details = detection_result.get("carro", [])

        if not car_details:
            return {"success": True, "message": "Nenhum carro identificado na imagem."}

        # Verifica se há infração
        has_infraction = car_details.get("tem_infracao", False)
        
        if not has_infraction:
            return {
                "success": True, 
                "data": {
                    "imagem": '/detect/' + detection_result.get("imagem")
                },
                "message": "Carro detectado, mas sem infração identificada.",
                "hasInfraction": False,
            }

        # -----------------------------------------------------
        # PROCESSAMENTO DA INFRAÇÃO
        # -----------------------------------------------------
        try:
            # Identificar tipo de infração no DB
            infraction_desc = car_details.get("infractions", [{}])[0].get("tipo")
            infraction_type_obj = db.query(models.TypeOfInfraction).filter(
                models.TypeOfInfraction.descricao == infraction_desc
            ).first()

            if not infraction_type_obj:
                return {"success": False, "message": f"Tipo de infração '{infraction_desc}' não cadastrado no sistema."}

            # Ler a placa (Resetando o cursor)
            await file.seek(0)
            retornoIa = await get_plate_function(file)
            placa = retornoIa.get("placa", "Não informado")
            cor = retornoIa.get("cor", "Não informado")
            
            # Busca carro existente ou cria um novo
            car_obj = get_or_create_vehicle(db, placa, cor)

            # Extrair Metadados e Localização
            await file.seek(0)
            metadata = await extract_image_metadata(file)

            infraction_address = None
            if metadata.get('local', {}):
                # Salvar Local da Infração no DB
                infraction_address = register_infraction_location_db(db, metadata)

            # Criar Registro da Infração
            final_infraction = create_infraction_record(
                db=db,
                image_path=detection_result.get("imagem"),
                car_id=car_obj.id,
                address_id=infraction_address.id if infraction_address else None,
                type_id=infraction_type_obj.id,
                user_id=user.id,
                data_infraction=metadata.get('metadados', {}).get('DateTime', '') if metadata.get('metadados', {}).get('DateTime', '') else None
            )

            infraction_data = schemas.InfractionsBase(
                data=final_infraction.data,
                imagem=final_infraction.imagem,
                veiculo=schemas.CarBase.model_validate(car_obj),
                endereco=schemas.AddressBase.model_validate(infraction_address) if infraction_address else None,
                tipo_infracao=schemas.TypeOfInfractionBase.model_validate(infraction_type_obj),
                user=schemas.UserResponse.model_validate(user)
            )

            return {
                "success": True,
                "message": "Infração registrada com sucesso.",
                "hasInfraction": True,
                "data": jsonable_encoder(infraction_data)
            }

        except Exception as e:
            print(f"Erro no processamento da infração: {e}")
            return {
                "success": False,
                "message": "Erro ao processar os dados da infração.",
                "error_details": str(e)
            }

    except Exception as e:
        return {
            "success": False,
            "message": "Erro interno no servidor.",
            "error_details": str(e)
        }