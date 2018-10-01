from flask import Flask, render_template, request, redirect
import os
import requests
import json
from requests_oauthlib import OAuth2
from dotenv import load_dotenv
import sys
load_dotenv()


# TODO check security and fail scenario, esp. for the authorize endpoint
try:
    client_id = os.environ['client_id']
    client_secret = os.environ['client_secret']
except KeyError:
    print("client id or secret not defined")
    raise

callback_uri = "http://termicoder.diveshuttam.me/authorize"

# TODO do everything with request-oauthlib
OAuth2()


app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
        SECRET_KEY='dev',
)

def log_user(access_token):
    users = []
    try:
        with open('users.json', 'r') as user_file:
            users = json.load(user_file)
    except:
            pass
    if(users is None or not isinstance(users,list)):
        users = []

    try:
        s = requests.session()
        OAuth2_Header = {
                'Authorization': 'Bearer %s' % access_token
        }
        s.headers.update(OAuth2_Header)
        username = s.get('https://api.codechef.com/users/me').json()['result']['data']['content']['username']
        print(username)
        if username not in users:
            users.append(username)
        with open('users.json', 'w') as user_file:
            json.dump(users, user_file)
    except BaseException:
        pass


# TODO implement give and check of state to make prevent cross site forgry
@app.route("/")
def index():
    authorize_url = "https://api.codechef.com/oauth/authorize"
    data = {
        "response_type": "code",
        "client_id": client_id,
        "state": "xyz",
        "redirect_uri": callback_uri
    }
    authorization_redirect_url = requests.Request(
        'get', authorize_url, params=data).prepare().url
    sys.stdout.flush()
    return render_template("index.html", url=authorization_redirect_url)


@app.route("/authorize")
def authorize():
    headers = {
        'content-Type': 'application/json',
    }
    token_url = "https://api.codechef.com/oauth/token"
    code = request.args.get('code')
    state = request.args.get('state')
    print(state)
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
        response = json.loads(access_token_response.text.strip())
        print(response)
        pretty_result = json.dumps(response, indent=4)
        access_token_response.raise_for_status()
        data = response["result"]["data"]
        access_token = data["access_token"]
        print(access_token)
        try:
            log_user(access_token)
        except:
            pass
    except BaseException as e:
        print(e)
        return render_template('error.html', response=pretty_result)
    else:
        return render_template('authorize.html', response=pretty_result)


@app.route("/ppt")
def ppt():
    google_slide_link = 'https://docs.google.com/presentation/d/' + \
                        '1KRNxb7YnfM4xiUJN8dNx1JnbeW0z4j8j8LeXmaCmdq8/'
    return redirect(google_slide_link)


@app.route("/repository")
def repository():
    repository_link = 'https://github.com/termicoder/termicoder-beta'
    return redirect(repository_link)


@app.route("/videos")
def vedios():
    youtube_playlist_link = 'https://www.youtube.com/playlist?' + \
                            'list=PLFkjosN0kO0Hn8umdK-XUIz5IlvUqB6VK'
    return redirect(youtube_playlist_link)


@app.route('/asciinema')
def asciinema():
    asciinema_link = 'https://asciinema.org/~diveshuttam'
    return redirect(asciinema_link)

@app.route('/users')
def users():
    try:
        users=json.load(open('users.json'))
        assert(isinstance(users, list))
    except:
        return render_template('no_users.html')
    else:
        return render_template('users.html', users=users)

if __name__ == "__main__":
    app.run('0.0.0.0', port=int(80), debug=False)
