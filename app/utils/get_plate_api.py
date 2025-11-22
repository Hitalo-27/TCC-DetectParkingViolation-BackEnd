from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database import get_db
import base64
import httpx
from dotenv import load_dotenv
import os

GEMINI_API_KEY = os.getenv("GEMINI_KEY")
GEMINI_URL = os.getenv("GEMINI_URL")

async def get_plate_function(file: UploadFile):
    # 1. Ler a imagem
    image_bytes = await file.read()

    # 2. Converter a imagem para Base64
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')

    # 3. Montar o header
    headers = {
        "x-goog-api-key": GEMINI_API_KEY,
        "Content-Type": "application/json"
    }

    # 4. Montar o payload
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Leia o numero dessa placa de carro. Responda apenas com o numero e letra da placa, desconsidere os traços '-'."  
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

    # 5. Chamar a API do Gemini
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GEMINI_URL,
            json=payload,
            headers=headers,
            timeout=30.0
        )

        # Lança erro se status for 4xx ou 5xx
        response.raise_for_status()

        # 6. Resultado final
        gemini_response = response.json()
        
        return gemini_response["candidates"][0]["content"]["parts"][0]["text"]
