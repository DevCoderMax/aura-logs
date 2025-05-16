import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from db.stp_db import create_table
from routes.errors import router as errors_router

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar o banco de dados
create_table()

# Criar a aplicação FastAPI
app = FastAPI(
    title="Aura Logs API",
    description="API para análise e armazenamento de logs de erro",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique as origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(errors_router)

@app.get("/")
async def root():
    """Endpoint raiz da API."""
    return {"message": "Bem-vindo à API Aura Logs", "status": "online"}

# Iniciar a aplicação com uvicorn quando executado diretamente


