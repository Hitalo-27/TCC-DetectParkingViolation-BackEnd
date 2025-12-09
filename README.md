# 🚀 Backend Completo - TCC (FastAPI + MySQL + YOLOv11 + OpenCV)

## 🚗 Serviço de Detecção de Infrações de Estacionamento

Este repositório contém o backend completo do projeto desenvolvido em Python utilizando FastAPI, integrado com um serviço de visão computacional responsável pela detecção automática de infrações de estacionamento.

O projeto foi desenvolvido como parte do TCC da UNIP e tem como objetivo analisar imagens para identificar veículos e possíveis infrações, como estacionamento proibido ou irregular.

# 📌 Tecnologias Utilizadas
## 🖥️ Backend (API)

- Python 3.13+

- FastAPI

- MySQL

- SQLAlchemy

- Passlib (hash de senhas)

- Python-JOSE (autenticação com JWT)

## 🧠 Visão Computacional

- YOLOv11 (Ultralytics) – Detecção e segmentação de carros, placas e zonas proibidas

- OpenCV – Manipulação e processamento de imagens

- NumPy – Operações matemáticas de máscaras e cálculos

## 🧠 Como Funciona

O script carrega o modelo treinado (`best.pt`) e processa imagens de entrada. A lógica de infração é dividida em duas categorias:

1.  **Infração por Sobreposição (Interseção):**
    O script verifica se a máscara de pixels de um `carro` se sobrepõe (acima de um limite) com as máscaras de zonas proibidas, como:
    * `calcada`
    * `faixa_pedestre`
    * `guia_amarela` (meio-fio amarelo)
    * `guia_rebaixada` (entrada de garagem)
    * `rampa` (rampa de acessibilidade)

2.  **Infração Relacional (Proximidade):**

- Detecta se um carro está dentro da área de influência de uma placa de proibido estacionar, analisando:

    * distância entre centro do carro e da placa

    * proporção entre tamanhos

    * ângulo relativo


- Os resultados são exportados nas pastas:

    * resultados/        → processamento de múltiplas imagens
    * resultadoUnico/    → processamento de uma imagem

## ⚙️ Como Rodar Localmente (BACKEND + VISÃO COMPUTACIONAL)

1. Clone o repositório:
```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DA_PASTA_CLONADA>
```

2. Crie o banco de dados MySQL com o arquivo `schema.sql`:

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute a aplicação:
```bash
uvicorn app.main:app --reload
```

## 📚 Documentação da API

A documentação interativa (Swagger) está disponível em:

👉 ```http://127.0.0.1:8000/docs```

## 🖥️ Frontend do Projeto

O frontend do EcoDetect está disponível no repositório:

👉 ```https://github.com/Hitalo-27/TCC-DetectParkingViolation-FrontEnd```
