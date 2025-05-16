import requests
import json
import sys

# URL da API (ajuste a porta conforme configurado no api.py)
API_URL = "http://localhost:8097/errors/"

# Exemplo de dados de erro para teste
error_data = {
    "error_data": {
        "message": "TypeError: Cannot read property 'value' of undefined",
        "stack": "TypeError: Cannot read property 'value' of undefined\n    at processData (/app/src/utils/dataProcessor.js:42:23)\n    at Object.handleSubmit (/app/src/components/Form.js:105:12)\n    at HTMLUnknownElement.callCallback (/app/node_modules/react-dom/cjs/react-dom.development.js:3945:14)\n    at Object.invokeGuardedCallbackDev (/app/node_modules/react-dom/cjs/react-dom.development.js:3994:16)",
        "component": "Form.js",
        "timestamp": "2025-05-16T19:45:12Z",
        "user_id": "user_12345",
        "browser": "Chrome 120.0.0",
        "os": "Windows 11"
    },
    "context": "Erro ocorreu durante o envio do formulário de cadastro de usuário"
}

def test_post_error():
    """Testa o envio de dados de erro para a API."""
    try:
        print("Enviando dados de erro para a API...")
        response = requests.post(API_URL, json=error_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\nSucesso! Erro registrado com ID: {result['error_id']}")
            return result['error_id']
        else:
            print(f"\nErro na requisição: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"\nExceção ao chamar a API: {str(e)}")
        return None

def test_get_error(error_id):
    """Testa a recuperação de um erro específico pelo ID."""
    if not error_id:
        print("ID de erro não fornecido. Pulando teste de recuperação.")
        return
    
    try:
        print(f"\nRecuperando detalhes do erro com ID {error_id}...")
        response = requests.get(f"{API_URL}{error_id}")
        
        if response.status_code == 200:
            result = response.json()
            print("\nDetalhes do erro:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"\nErro ao recuperar detalhes: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"\nExceção ao recuperar erro: {str(e)}")

def test_list_errors():
    """Testa a listagem de todos os erros."""
    try:
        print("\nListando todos os erros...")
        response = requests.get(API_URL)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\nTotal de erros encontrados: {len(result)}")
            if result:
                print("\nÚltimo erro registrado:")
                print(json.dumps(result[0], indent=2, ensure_ascii=False))
        else:
            print(f"\nErro ao listar erros: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"\nExceção ao listar erros: {str(e)}")

if __name__ == "__main__":
    print("=== TESTE DA API AURA LOGS ===")
    
    # Testar POST para criar um novo erro
    error_id = test_post_error()
    
    # Testar GET para recuperar o erro criado
    if error_id:
        test_get_error(error_id)
    
    # Testar GET para listar todos os erros
    test_list_errors()
