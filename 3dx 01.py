import requests
import json

import passwords

#import nusername and npassword from passwords.py

unsername = passwords.nuser
password = passwords.npassword
passport = passwords.npassport

session = requests.Session()

# Get login ticket
url = passport + '/login?action=get_auth_params'
print('Requesting login ticket...')
response = session.get(url, verify=True)
data = json.loads(response.text)
login_ticket = str(data['lt'])
print(login_ticket)


