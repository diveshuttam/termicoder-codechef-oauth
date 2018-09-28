from flask import Flask, render_template, request
import os
import requests
import json
from requests_oauthlib import OAuth2
from dotenv import load_dotenv
load_dotenv()

try:
    client_id = os.environ['client_id']
    client_secret = os.environ['client_secret']
except KeyError:
    print("client id or secret not defined")
    raise

callback_uri = "http://termicoder.diveshuttam.me/authorize"

# TODO do everything with oauth2
OAuth2()


app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
        SECRET_KEY='dev',
)


@app.route("/")
def index():
    authorize_url = "https://api.codechef.com/oauth/authorize"
    data = {
        "response_type": "code",
        "client_id": client_id,
        "state": "xyz",
        "redirect_uri": callback_uri
    }
    authorization_redirect_url = requests.get(authorize_url, params=data).url
    print(authorization_redirect_url)
    return render_template("index.html", url=authorization_redirect_url)


@app.route("/authorize")
def authorize():
    headers = {
        'content-Type': 'application/json',
    }
    token_url = "https://api.codechef.com/oauth/token"
    code = request.args.get('code')
    state = request.args.get('state')
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': callback_uri
    }

    print("requesting access token")
    try:
        access_token_response = requests.post(
            token_url, data=json.dumps(data),
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
        return render_template('error.html', response=pretty_result)
    else:
        return render_template('authorize.html', response=pretty_result)


if __name__ == "__main__":
    app.run(debug=True)
