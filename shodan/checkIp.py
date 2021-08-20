import json

from shodan import Shodan


config = json.loads(input())
allData = json.loads(input())

if "payload" in allData:
    data = allData["payload"]

if "input_path" in config:
    input_path = config["input_path"]

    if len(input_path) > 0:
        if input_path in allData:
            data = allData[input_path]
        else:
            allData["payload"] = input_path + "doesn't exist in msg"
            print(json.dumps(allData))
            exit()

# check o/p path
if "output_path" in config and config["output_path"] != "":
    output_path = config["output_path"]
else:
    output_path = "payload"

apikey = config['apikey']
api = Shodan(apikey)

# Lookup an IP
try:
    if data and type(data) is str:
        ipinfo = api.host(data.strip())
        allData[output_path] = ipinfo
    elif data and type(data) is list:
        res = []
        for ip in data:
            if ip and type(ip) is str:
                res.append(api.host(ip.strip()))
        allData[output_path] = res
    else:
        allData[output_path] = 'Insufficient input'

    print(json.dumps(allData))
except Exception as e:
    allData[output_path] = {
        'error': str(e)
    }
    print(json.dumps(allData))