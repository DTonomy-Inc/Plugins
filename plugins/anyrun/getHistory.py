import requests
import json

config = json.loads(input())
allData = json.loads(input())

if('payload' not in allData):
    allData['payload'] = "No input."
    print(json.dumps(allData))
    exit()
    
data = allData['payload']

if data and type(data) is str:
    skip = data
    username = config['username']
    password = config['password']
elif config and type(config) is dict:
    username = config['username']
    password = config['password']
    if 'skip' in config:
        skip = config['skip']
else:
    print('Insufficient Data Input From Previous Node or Current Node')

if skip:
    url = 'https://api.any.run/v1/analysis/'
else:
    url = 'https://api.any.run/v1/analysis/?skip=' + skip

try:
    response = requests.get(url, auth=(username, password)
    allData['payload'] = response.content.decode("utf-8"))
except requests.exceptions.RequestException as error:  
    allData['payload'] = error

print(json.dumps(allData))

