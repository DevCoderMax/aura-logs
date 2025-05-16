from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from db.connection import insert_error, get_all_errors, get_error_by_id
from services.error_analyzer import analyze_error

router = APIRouter(prefix="/errors", tags=["errors"])

class ErrorRequest(BaseModel):
    error_data: Dict[str, Any]
    context: Optional[str] = None

class ErrorResponse(BaseModel):
    error_id: int

class ErrorDetail(BaseModel):
    id: int
    nome: str
    descricao: str
    data_insercao: str

@router.post("/", response_model=ErrorResponse)
async def create_error(error_request: ErrorRequest):
    """
    Recebe dados de erro, analisa e salva no banco de dados.
    Retorna apenas o ID do erro criado.
    """
    try:
        # Analisar o erro e gerar nome e descrição
        nome, descricao = await analyze_error(error_request.error_data, error_request.context)
        
        # Salvar no banco de dados
        error_id = insert_error(nome, descricao)
        
        return {"error_id": error_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar: {str(e)}")

@router.get("/", response_model=List[ErrorDetail])
async def list_errors():
    """
    Lista todos os erros salvos no banco de dados.
    """
    return get_all_errors()

@router.get("/{error_id}", response_model=ErrorDetail)
async def get_error(error_id: int):
    """
    Retorna detalhes de um erro específico pelo ID.
    """
    error = get_error_by_id(error_id)
    if not error:
        raise HTTPException(status_code=404, detail="Erro não encontrado")
    return error
