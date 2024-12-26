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
print("Requesting login ticket...")
response = session.get(url, headers={"Accept": "application/json"}, verify=True)

if response.status_code == 200:
    data = response.json()
    login_ticket = data.get("lt")
    print("Login ticket obtido:", login_ticket)

    # Realiza autenticação no CAS
    username_enc = quote(username, encoding="utf-8")
    password_enc = quote(password, encoding="utf-8")
    service_enc = quote(space, encoding="utf-8")  # Codifica o serviço
    post_data_str = f"lt={login_ticket}&username={username_enc}&password={password_enc}&service={service_enc}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    }
    auth_url = f"{passport}/login"
    print("Realizando autenticação no CAS...")
    auth_response = session.post(auth_url, data=post_data_str, headers=headers, allow_redirects=False)

    if auth_response.status_code == 302:
        # Verifica o cabeçalho Location para o redirecionamento
        redirect_url = auth_response.headers.get("Location")
        print("Redirecionado para:", redirect_url)

        if "ticket=" in redirect_url:
            print("Conexão com o serviço Space bem-sucedida!")
            print("Ticket no redirecionamento:", redirect_url.split("ticket=")[-1])
        else:
            print("Redirecionado, mas sem ticket de serviço. Verifique a configuração do CAS e do serviço.")
    else:
        print(f"Erro ao autenticar no CAS. Código de status: {auth_response.status_code}")
        print("Detalhes:", auth_response.text)
else:
    print(f"Erro ao obter login ticket. Código de status: {response.status_code}")
    print("Detalhes:", response.text)
