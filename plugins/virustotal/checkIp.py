import json
from virus_total_apis import PublicApi as VirusTotalPublicApi

config = json.loads(input())
allData = json.loads(input())
result = []
count = 0
simplified_output = False

if 'simplified_output' in config:
    simplified_output = config['simplified_output']

# Payload by default
if "payload" in allData:
    msgBody = allData['payload']

# Using custom input field from node
if "input" in config:
    input_path = config['input']
    if len(input_path) > 0:
        if input_path in allData:
            msgBody = allData[input_path]
        else:
            allData['payload'] = input_path + " does not exist in msg"
            print(json.dumps(allData))
            exit()

# Output field
if "output" in config:
    output_path = config['output']

# Check Api key
if 'apikey' in config:
    apikey = config['apikey']
else:
    print(json.dumps(allData))
    exit()

vt = VirusTotalPublicApi(apikey)

if output_path == "":
    output_path = 'payload'

try:
    if(type(msgBody) is str):
        allData[output_path] = vt.get_ip_report(msgBody.strip())
    elif(type(msgBody) is list):
        for ip in msgBody:
            count += 1
            # Limit of 4 messages per minute
            if count == 4:
                time.sleep(60)
            result.append(vt.get_ip_report(ip.strip()))
        allData[output_path] = result
    else:
        allData[output_path] = "Input type error."
    
    if simplified_output:
        try:
            for i in range(0, len(allData[output_path])):
                if 'response_code' in allData[output_path][i]:
                    del allData[output_path][i]['response_code']
                allData[output_path][i]['location'] = {}
                allData[output_path][i]['as_owner'] = {}
                allData[output_path][i]['detected_urls'] = {}
                allData[output_path][i]['resolutions'] = {}

                if 'results' in allData[output_path][i]:
                    if 'country' in allData[output_path][i]['results']:
                        allData[output_path][i]['location']['country'] = allData[output_path][i]['results']['country']
                    if 'continent' in allData[output_path][i]['results']:
                        allData[output_path][i]['location']['continent'] = allData[output_path][i]['results']['continent']
                    if 'network' in allData[output_path][i]['results']:
                        allData[output_path][i]['location']['network'] = allData[output_path][i]['results']['network']
                    if 'resolutions' in allData[output_path][i]['results']:
                        allData[output_path][i]['resolutions'] = allData[output_path][i]['results']['resolutions']    
                    if 'as_owner' in allData[output_path][i]['results']:
                        allData[output_path][i]['as_owner'] = allData[output_path][i]['results']['as_owner']
                    if 'detected_urls' in allData[output_path][i]['results']:
                        allData[output_path][i]['detected_urls'] = allData[output_path][i]['results']['detected_urls']
                    del allData[output_path][i]['results']

                if(type(msgBody) is list):
                    allData[output_path][i]['ip'] = msgBody[i]
                elif(type(msgBody) is str):
                    allData[output_path][i]['ip'] = msgBody
            
        except Exception as e:
            allData[output_path] = result

except:
    allData[output_path] = "Invalid input"       

print(json.dumps(allData))
