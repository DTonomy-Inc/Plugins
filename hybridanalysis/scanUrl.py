import json
import time
from invokeFalconSandboxWebApi import postFalconSandbox

config = json.loads(input())
allData = json.loads(input())
deep_scan = False
simplified_output = False
input_data = []
result = []
malicious_urls = []

if 'simplified_output' in config:
    simplified_output = config['simplified_output']

if 'deep_scan' in config:
    deep_scan = config['deep_scan']

if "output" in config:
    output_path = config['output']

if output_path == "":
    output_path = 'payload'

if('payload' not in allData):
    allData['payload'] = "No input."
    print(json.dumps(allData))
    exit()

if('urls' in allData):
    url_list = allData['urls']
    if len(url_list) == 0:
        print(json.dumps(allData))
        exit()

    for url in url_list:
        data = {
            'url': url,
            'scan_type': 'all'
        }
        input_data.append(data)
else:
    data = allData['payload']

    if data and type(data) is dict and 'url' in data:
        url = data['url']
    else:
        url = config['url']

    data = {
        'url': url,
        'scan_type': 'all'
    }
    input_data.append(data)

root = config['root']
apikey = config['apikey']

# This function will check only once if there are results
def resultAPI(root, apikey, input_data):
    for request in input_data:
        try:
            response = postFalconSandbox(
                root + '/api/v2/quick-scan/url-for-analysis', apikey, request)
        except:
            continue
        if response['scanners'][0]['status'] == 'in-queue':
            time.sleep(4)
            response = postFalconSandbox(
                root + '/api/v2/quick-scan/url-for-analysis', apikey, request)
            result.append(response)
        else:
            result.append(response)
    return result


# This function will keep trying iteratively(usually takes more than 15 second per result)
def resultAPIDeepScan(root, apikey, input_data):
    for request in input_data:
        try:
            response = postFalconSandbox(
                root + '/api/v2/quick-scan/url-for-analysis', apikey, request)
        except:
            continue
        while response['finished'] == False:
            time.sleep(4)
            response = postFalconSandbox(
                root + '/api/v2/quick-scan/url-for-analysis', apikey, request)
        result.append(response)
    return result


try:
    if deep_scan == True:
        result = resultAPIDeepScan(root, apikey, input_data)
    else:
        result = resultAPI(root, apikey, input_data)

    allData[output_path] = result

    if simplified_output:
        try:
            for i in range(0, len(allData[output_path])):
                allData[output_path][i]['virustotal'] = {}
                if 'scanners' in allData[output_path][i]:
                    del allData[output_path][i]['whitelist']
                    del allData[output_path][i]['finished']
                    del allData[output_path][i]['reports']
                    del allData[output_path][i]['sha256']
                    del allData[output_path][i]['id']

                    for j in range(0, len(allData[output_path][i]['scanners'])):
                        if 'status' in allData[output_path][i]['scanners'][j]:
                            if allData[output_path][i]['scanners'][j]['status'] == 'malicious':
                                allData['isMaliciousURL'] = True
                                malicious_urls.append(allData['urls'][i])
                                
                    allData[output_path][i]['virustotal'] = allData[output_path][i]['scanners'][0]
                    del allData[output_path][i]['scanners']

                if 'urls' in allData:
                    allData[output_path][i]['url'] = allData['urls'][i]
                else:
                    allData[output_path][i]['url'] = url
            allData['maliciousUrls'] = malicious_urls
        except Exception as e:
            allData[output_path] = result

     # if a single result then convert back to string to maintain backward compatibility
    if(len(allData[output_path]) == 1):
        allData[output_path] = allData[output_path][0]

    print(json.dumps(allData))
except Exception as e:
    allData[output_path] = {
        'error': str(e)
    }
    print(json.dumps(allData))
