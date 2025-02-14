from autenticacao_space import AutenticacaoSpace
import passwords
import requests
import json

# Configurações
username = passwords.nuser
password = passwords.npassword
passport_url = passwords.npassport
space_url = passwords.nspace
tenant = passwords.ntenant

# Your role, company, collab space
ROLE = 'VPLMProjectLeader'
COMPANY = 'Company Name'
COLLABORATIVE_SPACE = 'Kastner - Workshop'
SECURITY_CONTEXT = ROLE + '.' + COMPANY + '.' + COLLABORATIVE_SPACE

# Instância da classe de autenticação
autenticador = AutenticacaoSpace(username, password, passport_url, space_url)
session = requests.Session()

try:
    # Obter ticket de serviço
    ticket = autenticador.autenticar_no_cas()
    print("Ticket obtido:", ticket)
except Exception as e:
    print("Erro durante a autenticação:", str(e))
    exit()

# Item ID
id = '1F53D9FD80620000615F09DD00160A55'

# Search string
search_string = 'Kastner'

print(SECURITY_CONTEXT)

# Define web service URL, agora passando o ticket como parâmetro na URL
url = f"{space_url}/resources/v1/modeler/dseng/dseng:EngItem/search?tenant={tenant}&$searchStr={search_string}&$mask=dsmveng:EngItemMask.Details&$top=1000&$skip=0&ticket={ticket}"
print("URL final com ticket:", url)

# Use basic authorization (agent)
headers = {
    'Content-Type': 'application/json',
    'SecurityContext': SECURITY_CONTEXT
}
print(json.dumps(headers, indent=4))

print('Performing search for engineering items (Basic authentication)...')
print('Search string: ' + search_string)

# Realizar a requisição
response = session.get(url, headers=headers, verify=True)

# Verificar o status e o tipo de conteúdo da resposta
if response.status_code == 200:
    if "application/json" in response.headers.get("Content-Type", ""):
        text = response.json()
        print(json.dumps(text, indent=4))
    else:
        print("Resposta recebida não está em formato JSON.")
        print("Cabeçalhos da resposta:", response.headers)
        print("Conteúdo da resposta:", response.text)
else:
    print(f"Erro na requisição. Código de status: {response.status_code}")
    print("Detalhes:", response.text)
