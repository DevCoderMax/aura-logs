import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar o cliente da API Gemini
def get_genai_client():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY não encontrada nas variáveis de ambiente")
    return genai.Client(api_key=api_key)

async def analyze_error(error_data, context=None):
    """
    Analisa os dados de erro usando a IA do Google Gemini e retorna um nome e descrição para o erro.
    
    Args:
        error_data (dict): Dados do erro em formato JSON
        context (str, optional): Contexto adicional sobre o erro
        
    Returns:
        tuple: (nome, descrição) gerados pela IA
    """
    client = get_genai_client()
    model = "gemini-2.5-flash-preview-04-17"  # Usando o mesmo modelo do código original
    
    # Preparar o prompt para a IA
    error_json = json.dumps(error_data, indent=2)
    prompt = f"""Analise o seguinte erro e forneça:
1. Um nome curto e descritivo para o erro (máximo 50 caracteres)
2. Uma descrição detalhada do erro, incluindo possíveis causas e soluções

Dados do erro:
{error_json}
"""
    
    if context:
        prompt += f"\nContexto adicional:\n{context}"
    
    # Configurar a solicitação para a IA
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        ),
    ]
    
    system_instruction = """Você é um analisador de logs de erros especializado. 
    Sua tarefa é analisar os dados de erro fornecidos e gerar:
    1. Um nome curto e descritivo para o erro (máximo 50 caracteres)
    2. Uma descrição detalhada do erro, incluindo possíveis causas e soluções
    
    Responda no seguinte formato JSON:
    {
        "nome": "Nome curto do erro",
        "descricao": "Descrição detalhada do erro, incluindo possíveis causas e soluções"
    }
    """
    
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        system_instruction=[types.Part.from_text(text=system_instruction)],
    )
    
    # Fazer a solicitação para a IA
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    
    try:
        # Extrair nome e descrição da resposta
        result = json.loads(response.text)
        nome = result.get("nome", "Erro não classificado")
        descricao = result.get("descricao", "Sem descrição disponível")
        
        return nome, descricao
    except Exception as e:
        # Fallback em caso de erro no parsing
        return "Erro na análise", f"Não foi possível analisar o erro corretamente: {str(e)}"
