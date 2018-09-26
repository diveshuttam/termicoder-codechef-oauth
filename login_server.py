from flask import Flask, abort, request
import os
import requests
import json
from requests_oauthlib import OAuth2

authorization_code = None

# TODO get token_callback_uri from the request
token_callback_uri = "http://127.0.0.1:8000/"
headers = {
    'content-Type': 'application/json',
}

data = {
    'grant_type': 'authorization_code',
    'code': authorization_code,
    'client_id': os.environ['client_id'],
    'client_secret': os.environ['client_secret'],
    'redirect_uri': token_callback_uri
}

print("requesting access token")
access_token_response = requests.post('https://api.codechef.com/oauth/token',
                                      data=json.dumps(data), headers=headers)

tokens = json.loads(access_token_response.text)
result = tokens["result"]
data = result["data"]
access_token = data["access_token"]

# TODO do everything with oauth2
OAuth2()

if __name__ == "__main__":
    pass
