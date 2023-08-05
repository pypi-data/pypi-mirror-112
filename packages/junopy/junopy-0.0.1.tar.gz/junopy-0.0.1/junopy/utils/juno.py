
from junopy.utils import constants
import base64
import requests

TOKEN = {}
SANDBOX = True
CLIENTID = ''
CLIENTSECRET = ''

def Juno(access_token, clientId, clientSecret, sandbox=True):
    global TOKEN
    global SANDBOX
    global CLIENTID
    global CLIENTSECRET
    SANDBOX = sandbox
    CLIENTID = clientId
    CLIENTSECRET = clientSecret
    TOKEN['PRIVATE'] = access_token

def GetToken():
    hash = base64.b64encode(f'{CLIENTID}:{CLIENTSECRET}'.encode("utf-8")).decode("utf-8")
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {hash}'
    }
    route = constants.ROUTE_SANDBOX_AUTORIZATION_SERVER if SANDBOX else constants.ROUTE_PRODUCAO_AUTORIZATION_SERVER
    response = __ValidateResponse(requests.post(route, headers=headers, data={'grant_type':'client_credentials'}))
    TOKEN['TOKEN']  = response['access_token']
    TOKEN['TYPE']  = response['token_type']
    TOKEN['EXPIRES'] = response['expires_in']

def __headers():
    if not 'TYPE' in TOKEN or not 'TOKEN' in TOKEN or not 'EXPIRES' in TOKEN:
        GetToken()
    __headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'X-Api-Version': '2',
        'X-Resource-Token': f"{TOKEN['PRIVATE']}",
        'Authorization': f"{TOKEN['TYPE']} {TOKEN['TOKEN']}"
    }
    return __headers

def __Route(url):
    route = constants.ROUTE_SANDBOX if SANDBOX else constants.ROUTE_PRODUCAO
    return f'{route}{url}'

def Get(url, data={}):
    return __ValidateResponse(requests.get(__Route(url), data=data, headers=__headers()))

def Post(url, data):
    return __ValidateResponse(requests.post(__Route(url), json=data, headers=__headers()))

def Put(url, data):
    return __ValidateResponse(requests.put(__Route(url), json=data, headers=__headers()))

def Patch(url, data):
    return __ValidateResponse(requests.patch(__Route(url), json=data, headers=__headers()))

def Delete(url):
    return __ValidateResponse(requests.delete(__Route(url), headers=__headers()))

class RequestException(Exception):
    def __init__(self, msg, errors):
        Exception.__init__(self, msg)

def __ValidateResponse(response):
    if response.status_code == 200 or response.status_code == 201:
        return response.json()
    elif response.status_code != 204:
        status_code = response.status_code
        try:
            response_json = response.json()
        except Exception as e:
            response_json = {'errors': [{'description': 'JUNO ERROR: ' + str(e)}]}
        error_message = f"JUNO REQUEST ERROR: Status {str(status_code)} \n Request not sent. May contain errors as missing required parameters or transcription error. \n {response_json}"
        raise RequestException(error_message, response_json)
