import requests


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
        else:
            raise Exception(f"Erro ao acessar o CAS. Código: {response.status_code}, Detalhes: {response.text}")

    def autenticar_no_cas(self):
        """
        Autentica no CAS e retorna o ticket de serviço (ST).
        """
        try:
            # Obter login ticket
            login_ticket = self.obter_login_ticket()

            # Usar o service diretamente, sem codificar
            service_encoded = self.space_url

            # Dados para autenticação
            payload = {
                "lt": login_ticket,
                "username": self.username,
                "password": self.password,
                "service": service_encoded,
            }
            headers = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}

            # Log do payload enviado
            # print("Payload enviado para autenticação:", payload)

            # Realizar autenticação
            auth_url = f"{self.passport_url}/login"
            response = self.session.post(auth_url, data=payload, headers=headers, allow_redirects=False)

            if response.status_code == 302:
                # Obter o redirecionamento
                redirect_url = response.headers.get("Location")
                print("URL de redirecionamento:", redirect_url)

                if "ticket=" in redirect_url:
                    ticket = redirect_url.split("ticket=")[-1]
                    return ticket

                # Diagnóstico adicional
                print("Redirecionamento bem-sucedido, mas sem ticket no destino:", redirect_url)
                raise Exception("Erro: Ticket de serviço não encontrado no redirecionamento.")
            elif response.status_code == 200:
                # Tratar casos onde o CAS responde com 200 (possível falha)
                print("Resposta 200 recebida. Verifique o redirecionamento ou a configuração do serviço.")
                print("Corpo da resposta:", response.text)
                raise Exception("CAS respondeu com 200. Possível falha de autenticação ou configuração incorreta.")
            else:
                # Outros erros
                print("Erro ao autenticar no CAS.")
                print("Código de status:", response.status_code)
                print("Cabeçalhos:", response.headers)
                print("Corpo:", response.text)
                raise Exception(f"Erro inesperado. Código: {response.status_code}")
        except Exception as e:
            raise Exception(f"Erro durante o processo de autenticação no CAS: {str(e)}")
