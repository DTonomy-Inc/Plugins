import json
from virus_total_apis import PublicApi as VirusTotalPublicApi

config = json.loads(input())

allData = json.loads(input())

if('payload' not in allData):
    allData['payload'] = "No input."
    print(json.dumps(allData))
    exit()
    
data = allData['payload']

if type(data) is str:
    url = data
elif type(config) is dict and 'url' in config:
    url = config['url']
else:
    print("Insufficient input")

apikey = config['apikey']
vt = VirusTotalPublicApi(apikey)

allData['payload'] = vt.get_url_report(url)
print(json.dumps(allData))
