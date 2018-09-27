from flask import Flask, render_template
import os
import requests
import json
from requests_oauthlib import OAuth2


# TODO get token_callback_uri from the request
token_callback_uri = "http://127.0.0.1:8000/"
headers = {
    'content-Type': 'application/json',
}

try:
    client_id = os.environ['client_id']
    client_secret = os.environ['client_secret']
except KeyError:
    print("client id not defined")
    raise


# TODO do everything with oauth2
OAuth2()


app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
        SECRET_KEY='dev',
)


@app.route("/<string:authorization_code>")
def index(authorization_code):
    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': token_callback_uri
    }

    print("requesting access token")
    try:
        access_token_response = requests.post(
            'https://api.codechef.com/oauth/token', data=json.dumps(data),
            headers=headers)
        response = access_token_response.text
        print(response)
        tokens = json.loads(response.strip())
        result = tokens["result"]
        pretty_result = json.dumps(result, indent=4)
        access_token_response.raise_for_status()
        data = result["data"]
        access_token = data["access_token"]
        print(access_token)
    except BaseException as e:
        print(e)
        return render_template('error.html', error=pretty_result)
    else:
        return render_template('index.html', response=pretty_result)


if __name__ == "__main__":
    app.run(debug=True)
