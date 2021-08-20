import json
from invokeFalconSandboxWebApi import postFalconSandbox

config = json.loads(input())

allData = json.loads(input())

if('payload' not in allData):
    allData['payload'] = "No input."
    print(json.dumps(allData))
    exit()
    
data = allData['payload']

if data and type(data) is dict and 'url' in data:
    url = data['url']
else:
    url = config['url']
root = config['root']
apikey = config['apikey']
data = {
    'url': url,
    'scan_type': 'all'
}

try:
    response = postFalconSandbox(root + '/api/v2/quick-scan/url-to-file', apikey, data)
    allData['payload'] = response
    print(json.dumps(allData))
except Exception as e:
    allData['payload'] = {
        'error': str(e)
    }
    print(json.dumps(allData))