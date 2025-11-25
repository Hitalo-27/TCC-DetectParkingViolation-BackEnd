# app/platereq.py
import requests
from typing import Any, Dict
import os
from dotenv import load_dotenv



API_URL = os.getenv("RADARCONSULTAS_URL") 

# 🔐 Credenciais (substitua pelos valores reais)
USERNAME =  os.getenv("RADAR_NAME")
PASSWORD = os.getenv("RADAR_PASSWORD")

def dadosveiculo(placa: str) -> Dict[str, Any]:
    """
    Envia POST para a API externa com JSON {"placa": placa}
    usando autenticação Basic Auth.
    """
    payload = {"placa": placa}

    try:
        # Envia POST com JSON e autenticação
        response = requests.post(
            API_URL,
            json=payload,
            auth=(USERNAME, PASSWORD),  
            timeout=15
        )

        # Levanta erro se status != 200
        response.raise_for_status()

        # Retorna o JSON da resposta
        return response.json()

    except requests.exceptions.RequestException as e:
        detalhe = {"error": "request_exception", "message": str(e)}
        if hasattr(e, "response") and e.response is not None:
            detalhe["status_code"] = e.response.status_code
            detalhe["response_text"] = e.response.text
        return detalhe

    except ValueError:
        # Caso a resposta não seja JSON
        return {"error": "invalid_json", "raw_text": response.text if 'response' in locals() else None}
