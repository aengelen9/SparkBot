import requests
import json
import ssl

from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#----------------------------------------------------------------
#DEVNET-DNAC LOGIN INFORMATION
#----------------------------------------------------------------
USER = "devnetuser"
PASSWORD = "Cisco123!"
URL = "https://sandboxdnac.cisco.com"
DNAC_AUTH = HTTPBasicAuth(USER, PASSWORD)

#----------------------------------------------------------------

#----------------------------------------------------------------
#METHODS
#----------------------------------------------------------------
def login():
    '''
    Performs a login to DNA Center
    '''
    requrl = URL + '/api/system/v1/auth/login'
    header = {'content-type': 'application/json'}
    response = requests.get(requrl, auth=DNAC_AUTH, headers=header, verify=False)
    response_header = response.headers
    cookie = response_header['Set-Cookie']
    return cookie


def get_network_devices(cookie):
    '''
    Gets a list of all network devices managed by DNA Center
    '''
    requrl = URL + '/api/v1/network-device'
    header = {'content-type': 'application/json', 'Cookie': cookie}
    response = requests.get(requrl, headers=header, verify=False)
    all_device_info = response.json()
    return all_device_info['response']

def get_nw_device_by_id(cookie, id):
    '''
    Gets a list of all network devices managed by DNA Center
    '''
    requrl = URL + '/api/v1/network-device/' + id
    header = {'content-type': 'application/json', 'Cookie': cookie}
    response = requests.get(requrl, headers=header, verify=False)
    device_info = response.json()
    return device_info['response']

def get_hosts(cookie):
    '''
    Gets a list of all hosts monitored by DNA Center
    '''
    requrl = URL + '/api/v1/host'
    header = {'content-type': 'application/json', 'Cookie': cookie}
    response = requests.get(requrl, headers=header, verify=False)
    all_device_info = response.json()
    return all_device_info['response']

def getHost(cookie, macAddr):
    '''
    Gets host with MAC address
    '''
    requrl = URL + '/api/v1/host'
    header = {'content-type': 'application/json', 'Cookie': cookie}
    filtr = {"hostMac":macAddr}
    response = requests.get(requrl, headers=header, params=filtr, verify=False)
    all_device_info = response.json()
    return all_device_info['response']

def getModule(cookie, id):
    '''
    Gets a list of all network devices managed by DNA Center
    '''
    requrl = URL + '/api/v1/network-device/module/' + id
    header = {'content-type': 'application/json', 'Cookie': cookie}
    response = requests.get(requrl, headers=header, verify=False)
    device_info = response.json()
    return device_info['response']

def getClientTime(cookie):
    '''
    Get Client Time
    '''
    requrl = URL + '/api/assurance/v1/time'
    header = {'content-type': 'application/json', 'Cookie': cookie}
    response = requests.get(requrl, headers=header, verify=False)
    clientTime = response.json()
    return clientTime['response'][1]['time']

def getClientHealth(cookie, macAddr, clientTime):
    '''
    Get Client Health
    '''
    requrl = URL + '/api/assurance/v1/host/' + macAddr + '?timestamp=' + clientTime
    header = {'content-type': 'application/json', 'Cookie': cookie}
    response = requests.get(requrl, headers=header, verify=False)
    clientHealth = response.json()
    return clientHealth['response'][0]
