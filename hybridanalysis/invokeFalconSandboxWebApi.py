import json
import requests
import urllib.parse
import urllib.request


def getFalconSandbox(url, apiKey):
    req = urllib.request.Request(url)
    req.add_header('api-key', apiKey)
    req.add_header('User-Agent', 'Falcon Sandbox')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')

    with urllib.request.urlopen(req) as response:
        json_response = json.loads(response.read().decode('utf-8'))
    return json_response


def postFalconSandbox(url, apiKey, data):
    data = urllib.parse.urlencode(data)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data=data)
    req.add_header('api-key', apiKey)
    req.add_header('User-Agent', 'Falcon Sandbox')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')

    with urllib.request.urlopen(req) as response:
        json_response = json.loads(response.read().decode('utf-8'))
    return json_response


def postFalconSandboxFile(url, apiKey, payload, files):
    headers = {
        'api-key': apiKey,
        'accept': 'application/json',
        'user-agent': 'Falcon Sandbox'
    }
    response = requests.request(
        "POST", url, headers=headers, data=payload, files=files)
    return json.loads(response.text)
