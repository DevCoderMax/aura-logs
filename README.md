# Aura Logs

Sistema de análise e armazenamento de logs de erro para o Aura.

## Descrição

Esta API recebe informações de erro em formato JSON, utiliza IA (Google Gemini) para analisar o erro e gerar um nome e descrição, e armazena essas informações em um banco de dados SQLite local.

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/DevCoderMax/aura-logs.git
   cd aura-logs
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env e adicione sua chave de API do Google Gemini
   ```

## Uso

1. Inicie o servidor:
   ```bash
   python api.py
   ```

2. A API estará disponível em `http://localhost:8000`

3. Documentação da API estará disponível em `http://localhost:8000/docs`

## Endpoints

### POST /errors/

Envia informações de erro para análise e armazenamento.

**Corpo da requisição:**
```json
{
  "error_data": {
    "message": "Error message",
    "stack": "Stack trace...",
    "additional_info": "..."
  },
  "context": "Contexto opcional do erro"
}
```

**Resposta:**
```json
{
  "error_id": 1
}
```

### GET /errors/

Retorna todos os erros armazenados.

### GET /errors/{error_id}

Retorna detalhes de um erro específico pelo ID.
