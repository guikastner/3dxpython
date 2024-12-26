import requests
from urllib.parse import quote


class AutenticacaoSpace:
    def __init__(self, username, password, passport_url, space_url):
        """
        Inicializa a classe de autenticação com os dados fornecidos.
        """
        self.username = username
        self.password = password
        self.passport_url = passport_url
        self.space_url = space_url
        self.session = requests.Session()

    def obter_login_ticket(self):
        """
        Obtém o login ticket (lt) do CAS.
        """
        url = f"{self.passport_url}/login?action=get_auth_params"
        response = self.session.get(url, headers={"Accept": "application/json"}, verify=True)
        if response.status_code == 200:
            login_ticket = response.json().get("lt")
            if login_ticket:
                return login_ticket
            raise Exception("Erro: Não foi possível obter o login ticket.")
        raise Exception(f"Erro ao acessar o CAS. Código: {response.status_code}, Detalhes: {response.text}")

    def autenticar_no_cas(self):
        """
        Autentica no CAS e retorna o ticket de serviço (ST).
        """
        # Obter login ticket
        login_ticket = self.obter_login_ticket()

        # Construir a URL do serviço
        service_encoded = quote(self.space_url, encoding="utf-8")

        # Dados para autenticação
        payload = {
            "lt": login_ticket,
            "username": quote(self.username),
            "password": quote(self.password),
            "service": service_encoded,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}

        # Realizar autenticação
        auth_url = f"{self.passport_url}/login"
        response = self.session.post(auth_url, data=payload, headers=headers, allow_redirects=False)

        if response.status_code == 302:
            redirect_url = response.headers.get("Location")
            if "ticket=" in redirect_url:
                ticket = redirect_url.split("ticket=")[-1]
                return ticket
            raise Exception("Erro: Ticket de serviço não encontrado no redirecionamento.")
        raise Exception(f"Erro ao autenticar no CAS. Código: {response.status_code}, Detalhes: {response.text}")