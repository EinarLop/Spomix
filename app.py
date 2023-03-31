import os
import base64
from flask import Flask, redirect, request
import requests

app = Flask(__name__)

access_token = ""

@app.route("/")
def get_artist():
    # new_artist = artist()
    return "Hello World"


@app.route("/login")
def get_login():
    client_id = f'client_id={os.environ.get("client_id")}'
    redirect_uri = f'redirect_uri={os.environ.get("redirect_uri")}'
    state = 'state=12355444444'
    scope = 'scope=user-read-private user-read-email user-top-read'
    response_type = 'response_type=code'
    return redirect(f'https://accounts.spotify.com/authorize?{client_id}&{redirect_uri}&{state}&{scope}&{response_type}')


@app.route("/callback")
def get_callback():
    code = request.args.get('code')
    state = request.args.get('state')
    payload = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': {os.environ.get("redirect_uri")}}
    message = f'{os.environ.get("client_id")}:{os.environ.get("client_secret")}'
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': "Basic " + base64.b64encode(message.encode("utf-8")).decode("utf-8")}

    r = requests.post('https://accounts.spotify.com/api/token', data=payload, headers=headers)
    rj = r.json()
    global access_token
    access_token = rj["access_token"]
    return "Token"


@app.route("/me")
def get_me():
    headers = {'Authorization': "Bearer " + access_token}
    r = requests.get('https://api.spotify.com/v1/me', headers=headers)
    return r.text


@app.route("/me/artists")
def get_me_artists():
    headers = {'Authorization': "Bearer " + access_token}
    r = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers)
    print(r)
    return r.text


@app.route("/me/tracks")
def get_me_tracks():
    headers = {'Authorization': "Bearer " + access_token}
    r = requests.get('https://api.spotify.com/v1/me/top/tracks', headers=headers)
    print(r)
    return r.text

