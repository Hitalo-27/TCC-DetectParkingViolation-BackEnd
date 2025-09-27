from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import users

# Criar tabelas no banco
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Backend em Python")

# Configurar CORS para permitir o frontend Next.js (localhost:3000)
origins = [
    "http://localhost:3000",  # endereço do seu frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # pode usar ["*"] para liberar todos os domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rotas
app.include_router(users.router)

@app.get("/")
def root():
    return {"msg": "API rodando com sucesso 🚀"}
