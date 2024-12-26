from autenticacao_space import AutenticacaoSpace
import passwords

# Configurações
username = passwords.nuser
password = passwords.npassword
passport_url = passwords.npassport
space_url = passwords.nspace

# Instância da classe de autenticação
autenticador = AutenticacaoSpace(username, password, passport_url, space_url)

try:
    # Obter ticket de serviço
    ticket = autenticador.autenticar_no_cas()
    print("Ticket obtido:", ticket)
except Exception as e:
    print("Erro durante a autenticação:", str(e))
