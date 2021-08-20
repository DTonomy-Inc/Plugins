import json
import time
from invokeFalconSandboxWebApi import postFalconSandboxFile

config = json.loads(input())
allData = json.loads(input())
output_path = ""
result = []
malicious_attachments = []
response = ""
deep_scan = False
simplified_output = True

if 'simplified_output' in config:
    simplified_output = config['simplified_output']

if 'deep_scan' in config:
    deep_scan = config['deep_scan']

# Payload by default
if "payload" in allData:
    data = allData['payload']

# if using input field from node
if "input" in config:
    input_path = config['input']
    if len(input_path) > 0:
        if input_path in allData:
            data = allData[input_path]
        else:
            allData['payload'] = input_path + " does not exist in msg"
            print(json.dumps(allData))
            exit()

if "output" in config:
    output_path = config['output']

root = config['root']
apikey = config['apikey']


# This function will check only once if there are results
def resultAPI(root, apikey, payload, files):
    response = postFalconSandboxFile(
        root + '/api/v2/quick-scan/file', apikey, payload, files)
    if response['scanners'][1]['status'] == 'in-queue':
        time.sleep(10)
        response = postFalconSandboxFile(
            root + '/api/v2/quick-scan/file', apikey, payload, files)
    return response


# This function will keep trying iteratively(usually takes more than 30 second per result)
def resultAPIDeepScan(root, apikey, payload, files):
    response = postFalconSandboxFile(
        root + '/api/v2/quick-scan/file', apikey, payload, files)
    time.sleep(10)
    while response['finished'] == False:
        time.sleep(10)
        response = postFalconSandboxFile(
            root + '/api/v2/quick-scan/file', apikey, payload, files)
    return response


try:
    # If allAttachments is passed from parseNestedEml
    if type(data) is list:
        for item in data:
            if type(item) is dict:
                if 'content' in item:
                    if 'data' in item['content']:
                        # data field created in python    
                        payload = {
                            'scan_type': 'all'
                        }
                        data = bytes(item['content']['data'])
                        files = [
                            ('file', data)
                        ]
                        if deep_scan == False:
                            try:
                                response = resultAPI(root, apikey, payload, files)
                            except:
                                continue
                        else:
                            try:
                                response = resultAPIDeepScan(
                                    root, apikey, payload, files)
                            except:
                                continue
                        result.append(response)

    elif type(data) is str:
        # if individual attachment is passed directly as byte string
        result = ""
        files = [
            ('file', data)
        ]
        if deep_scan == False:
            response = resultAPI(root, apikey, payload, files)
        else:
            response = resultAPIDeepScan(root, apikey, payload, files)
        result = response

except Exception as e:
    allData['payload'] = "Could not scan file"

if output_path != "":
    allData[output_path] = result
else:
    allData['payload'] = result

if simplified_output:
    try:
        for i in range(0, len(allData[output_path])):
            if 'scanners' in allData[output_path][i]:
                del allData[output_path][i]['whitelist']
                del allData[output_path][i]['finished']
                del allData[output_path][i]['reports']
                del allData[output_path][i]['id']
                del allData[output_path][i]['sha256']

                for j in range(0, len(allData[output_path][i]['scanners'])):
                    if 'status' in allData[output_path][i]['scanners'][j]:
                        if allData[output_path][i]['scanners'][j]['status'] == 'malicious':
                            allData['isMaliciousAttachment'] = True
                            if 'allAttachments' in allData:
                                if 'filename' in allData['allAttachments'][i]:
                                    malicious_attachments.append(allData['allAttachments'][i]['filename'])
                                else:
                                    malicious_attachments.append('')
            
            if 'allAttachments' in allData:
                if 'filename' in allData['allAttachments'][i]:
                    allData[output_path][i]['file'] = allData['allAttachments'][i]['filename']
                else:
                    allData[output_path][i]['file'] = ''

                if 'contentType' in allData['allAttachments'][i]:
                    allData[output_path][i]['file type'] = allData['allAttachments'][i]['contentType']
                else:
                    allData[output_path][i]['file type '] = ''

        allData['maliciousAttachments'] = malicious_attachments
    except Exception as e:
        allData[output_path] = result

print(json.dumps(allData))
