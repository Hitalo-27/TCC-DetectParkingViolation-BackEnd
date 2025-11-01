from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from ..database import get_db
import os
from dotenv import load_dotenv
import base64
import httpx

UPLOAD_DIR = "app/uploads"
UPLOAD_DIR_RELATIVE = "uploads"

router = APIRouter(prefix="/plate", tags=["veiculos"])

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_KEY")
GEMINI_URL = os.getenv("GEMINI_URL")

# Body -> Multipart -> file = imagem
@router.post("/identification")
async def get_plate(file: UploadFile = File(...)):
    
    try:
        image_bytes = await file.read()
        
        # Convertendo a imagem em BASE64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # Chave de acesso
        headers = {
            "x-goog-api-key": GEMINI_API_KEY,
            "Content-Type": "application/json" 
        }        
        
        payload = {
          "contents": [
            {
              "parts": [
                {
                  "text": "Leia o numero dessa placa de carro. Responda apenas com o numero da placa."
                },
                {
                  "inlineData": {
                    "mimeType": file.content_type,
                    "data": image_base64
                  }
                }
              ]
            }
          ]
        }  
              
        async with httpx.AsyncClient() as client:
            # A 'await' aqui é a chamada de rede, que não vai bloquear o servidor
            response = await client.post(
                GEMINI_URL, 
                json=payload, 
                headers=headers,  
                timeout=30.0
            )
            
            # 5. Tratar erros da API
            # Isso vai disparar um erro se a resposta for 4xx ou 5xx
            response.raise_for_status() 
        
            # 6. Extrair a resposta
            gemini_response = response.json()  
            
        placa = gemini_response["candidates"][0]["content"]["parts"][0]["text"]  
        
        print(f"Response: {placa}")    
        
        return {"placa_identificada": placa.strip()}
    except httpx.HTTPStatusError as e:
            # Erro específico se a API do Gemini retornar um erro (4xx, 5xx)
            print(f"Erro na API do Gemini: {e.response.text}")
            return JSONResponse(
                status_code=e.response.status_code, 
                content={"erro": "Falha ao processar imagem", "error => ": e.response.json()}
            )
    except httpx.RequestError as e:
            # Erro de rede (ex: timeout, não conseguiu conectar)
        print(f"Falha ao processar imagem, servidor não respondeu: {e}")
        return JSONResponse(
            status_code=503, # Service Unavailable
            content={"erro": "Não foi possível conectar ao serviço", "error => ": str(e)}
        )
    except Exception as e:
        # Erro genérico (ex: falha ao ler o arquivo, falha no base64, etc)
        print(f"Erro inesperado: {e}")
        return JSONResponse(status_code=500, content={"erro": "Erro interno no servidor", "error => ": str(e)})    
