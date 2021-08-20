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
    hash = data
elif type(config) is dict and 'hash' in config:
    hash = config['hash']
else:
    print("Insufficient input")

apikey = config['apikey']
vt = VirusTotalPublicApi(apikey)

allData['payload'] = vt.get_file_report(hash)
print(json.dumps(allData))
