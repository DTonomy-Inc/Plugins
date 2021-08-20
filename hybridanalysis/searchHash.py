import json
from invokeFalconSandboxWebApi import postFalconSandbox

config = json.loads(input())
allData = json.loads(input())
output_path = ""
result = []
response = []
    
# Payload by default
if "payload" in allData:
    input_hash = allData['payload']

# if using input field from node
if "input" in config:
    input_path = config['input']
    if len(input_path) > 0:
        if input_path in allData:
            input_hash = allData[input_path]
        else:
            allData['payload'] = input_path + " does not exist in msg"
            print(json.dumps(allData))
            exit()

# if using config
if 'hash' in config:
    if len(config['hash'])>0:
        input_hash = config['hash']

if "output" in config:
    output_path = config['output']

root = config['root']
apikey = config['apikey']

if type(input_hash) is str:
    data = {
        'hash': input_hash
    }
    result = ""
    result = data

if type(input_hash) is list:
    for item in input_hash:
        data = {
            'hash': item
        }
        result.append(data)

try:
    if type(result) is dict:
        response = ""
        response = postFalconSandbox(root + '/api/v2/search/hash', apikey, data)
        if not response:
            response.append("No result")
    elif type(result) is list:
        for value in result:
            item = postFalconSandbox(root + '/api/v2/search/hash', apikey, value)
            if not item:
                response.append("No result")
            else:
                response.append(item)
    
except Exception as e:
    allData['payload'] = {
        'error': str(e)
    }
    print(json.dumps(allData))

if output_path != "":
    allData[output_path] = response
else:
    allData['payload'] = response

print(json.dumps(allData))