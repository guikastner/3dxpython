import requests, json, base64
from passwords import PlatformCredentials

def get_login_session(): 
    """Perform CAS login using a persistant session object.
    1. Create session
    2. Get login ticket
    3. Login using username / password
    4. Return session object, will be used in subsequent calls (holds cookies etc)
    """

    session = requests.Session()
    
    # Get login ticket
    url = PlatformCredentials.passwordURL + '/login?action=get_auth_params'
    print('Requesting login ticket...')
    response = session.get(url, verify=True)
    data = json.loads(response.text)
    login_ticket = str(data['lt'])

    # CAS authentication
    url = SERVICE_3DPASSPORT + '/login'
    data = 'lt=' + login_ticket + '&username=' + USERNAME + '&password=' + PASSWORD + '&rememberMe=no'
    headers = {
        'tenant': TENANT,
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    print('Authenticating using CAS...')
    response = session.post(url, headers=headers, data=data, verify=True)
    return session
