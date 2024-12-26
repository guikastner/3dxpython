import requests
import json
from urllib.parse import quote
import passwords

# Importa username, password, passport e space do arquivo passwords.py
username = passwords.nuser
password = passwords.npassword
passport = passwords.npassport
space = passwords.nspace  # URL do serviço Space

# Inicializa a sessão
session = requests.Session()

# Obtem o login ticket
url = f"{passport}/login?action=get_auth_params"
print('Requesting login ticket...')
response = session.get(url, verify=True)

if response.status_code == 200:
    data = json.loads(response.text)
    login_ticket = str(data['lt'])
    print("Login ticket obtido:", login_ticket)

    # Codifica os parâmetros
    username_enc = quote(username, encoding="utf-8")
    password_enc = quote(password, encoding="utf-8")

    # Cria a string de dados para a requisição POST
    post_data_str = f"lt={login_ticket}&username={username_enc}&password={password_enc}"

    # Define os cabeçalhos da requisição
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    # URL para autenticação no CAS
    auth_url = f"{passport}/login"
    print("Realizando autenticação no CAS...")
    auth_response = session.post(auth_url, data=post_data_str, headers=headers)

    if auth_response.status_code == 200:
        # Verifica se há sucesso na autenticação
        print("Autenticação no CAS bem-sucedida. Conectando ao serviço...")

        # Codifica o URL do serviço TargetService (Space)
        target_service_enc = quote(space, encoding="utf-8")

        # URL para autenticar no serviço específico (Space)
        service_url = f"{passport}/login?service={target_service_enc}"
        service_response = session.get(service_url, headers=headers)

        # Verifica a resposta do serviço
        if service_response.status_code == 200:
            last_redirect_url = service_response.url  # URL final após redirecionamento
            if "ticket=" in last_redirect_url:
                print("Conexão com o serviço Space bem-sucedida!")
                print("Ticket recebido:", last_redirect_url.split("ticket=")[-1])
            else:
                print("Falha ao conectar ao serviço Space. Verifique as configurações.")
        else:
            print(f"Erro ao conectar ao serviço Space. Código de status: {service_response.status_code}")
    else:
        print(f"Erro ao autenticar no CAS. Código de status: {auth_response.status_code}")
else:
    print(f"Erro ao obter login ticket. Código de status: {response.status_code}")
