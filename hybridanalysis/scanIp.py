import json
import time
from invokeFalconSandboxWebApi import postFalconSandbox

config = json.loads(input())

allData = json.loads(input())
deep_scan = False
if 'deep_scan' in config:
    deep_scan = config['deep_scan']

if('payload' not in allData):
    allData['payload'] = "No input."
    print(json.dumps(allData))
    exit()

data = allData['payload']

if data and type(data) is dict and 'ip' in data:
    ip = data['ip']
else:
    ip = config['ip']
root = config['root']
apikey = config['apikey']
data = {
    'url': ip,
    'scan_type': 'all'
}

# This function will check only once if there are results
def resultAPI(root, apikey, data):
    response = postFalconSandbox(
        root + '/api/v2/quick-scan/url', apikey, data)
    # Ideally better to check if response['scanners'][finished] == false but for the free version just check status 'in-queue' for virus total to avoid maximum submissions
    if response['scanners'][0]['status'] == 'in-queue':
        time.sleep(4)
        response = resultAPI(root, apikey, data)
        # Not checking iteratively due to limitations of free version
        return response
    return response


# This function will keep trying iteratively(usually takes more than 15 second per result)
def resultAPIDeepScan(root, apikey, data):
    response = postFalconSandbox(
        root + '/api/v2/quick-scan/url', apikey, data)
    while response['finished'] == False:
        time.sleep(4)
        response = resultAPI(root, apikey, data)
    return response


try:
    response = resultAPI(root, apikey, data)
    if deep_scan == True:
        response = resultAPIDeepScan(root, apikey, data)
    else:
        response = resultAPI(root, apikey, data)
    allData['payload'] = response
    print(json.dumps(allData))
except Exception as e:
    allData['payload'] = {
        'error': str(e)
    }
    print(json.dumps(allData))
