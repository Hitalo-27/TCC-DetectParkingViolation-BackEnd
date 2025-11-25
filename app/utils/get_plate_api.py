import base64
import json
import re
import os
import httpx
from fastapi import UploadFile, HTTPException
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_KEY")

GEMINI_URL = os.getenv("GEMINI_URL") 

OCR_PROMPT = """
Atue como um especialista em visão computacional e OCR (Reconhecimento Óptico de Caracteres). Analise a imagem fornecida e extraia as informações do veículo seguindo rigorosamente as regras abaixo:

1. **Detecção:** Verifique se há um veículo na imagem, caso haja mais de um foque no veículo com mais destaque (maior e mais centralizado).
2. **Cor:** Identifique a cor predominante do veículo.
3. **Placa:** Se a placa estiver visível e legível:
   - Extraia apenas os caracteres alfanuméricos.
   - Remova hifens (-), espaços ou caracteres especiais.
   - Converta tudo para letras maiúsculas.
   - Limite a 7 caracteres.
4. **Ausência de dados:** Caso não haja veículo, ou a placa não esteja visível/legível, ou a cor não seja clara, preencha o campo respectivo com "Não Identificada".

**Formato de Saída:**
Responda EXCLUSIVAMENTE com um objeto JSON válido. Não inclua explicações ou texto antes/depois do JSON.

Estrutura do JSON:
{
  "placa": "STRING",
  "cor": "STRING"
}
"""

async def get_plate_function(file: UploadFile):
    try:
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
                        {"text": OCR_PROMPT},
                        {
                            "inlineData": {
                                "mimeType": file.content_type,
                                "data": image_base64
                            }
                        }
                    ]
                }
            ],
            # Configuração opcional para forçar resposta JSON (funciona melhor no Gemini 1.5 Pro/Flash)
            "generationConfig": {
                "response_mime_type": "application/json"
            }
        }

        # 5. Chamar a API do Gemini
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GEMINI_URL,
                json=payload,
                headers=headers,
                timeout=30.0
            )
            
            response.raise_for_status()
            gemini_response = response.json()

        # 6. Extrair o texto da resposta
        try:
            raw_text = gemini_response["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            raise HTTPException(status_code=502, detail="Resposta inválida do Gemini API")

        # 7. Limpar e Converter o texto para JSON (Python Dict)
        # O Gemini as vezes responde com ```json {dados} ```, precisamos limpar isso
        cleaned_text = re.sub(r"```json|```", "", raw_text).strip()
        
        vehicle_data = json.loads(cleaned_text)

        return vehicle_data

    except json.JSONDecodeError:
        # Caso a IA retorne texto puro em vez de JSON
        raise HTTPException(status_code=500, detail="Falha ao processar o JSON retornado pela IA.")
    except httpx.HTTPStatusError as e:
        print(f"Erro na API Gemini: {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail="Erro de comunicação com Gemini API")
    except Exception as e:
        print(f"Erro interno: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))