import os
import base64
from flask import Flask, redirect, request
import requests

import firebasefunctions
import helperfunctions
from firebaseconfig import *
from firebasefunctions import *

app = Flask(__name__)

access_token = ""
refresh_token = ""
seeds = []


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
    return redirect(
        f'https://accounts.spotify.com/authorize?{client_id}&{redirect_uri}&{state}&{scope}&{response_type}')


@app.route("/callback")
def get_callback():
    code = request.args.get('code')
    state = request.args.get('state')
    payload = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': {os.environ.get("redirect_uri")}}
    message = f'{os.environ.get("client_id")}:{os.environ.get("client_secret")}'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Authorization': "Basic " + base64.b64encode(message.encode("utf-8")).decode("utf-8")}

    r = requests.post('https://accounts.spotify.com/api/token', data=payload, headers=headers)
    rj = r.json()

    current_access_token = rj["access_token"]
    current_refresh_token = rj["refresh_token"]

    user_id = helperfunctions.get_me(current_access_token)

    firebasefunctions.set_user(user_id, current_refresh_token)

    return current_access_token, user_id


@app.route("/refresh")
def refresh():
    message = f'{os.environ.get("client_id")}:{os.environ.get("client_secret")}'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Authorization': "Basic " + base64.b64encode(message.encode("utf-8")).decode("utf-8")}
    global access_token
    global refresh_token

    payload = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}
    r = requests.post('https://accounts.spotify.com/api/token', data=payload, headers=headers)
    rj = r.json()
    access_token = rj["access_token"]
    return "Refreshed Token"


@app.route("/me")
def get_me(current_access_token):
    headers = {'Authorization': "Bearer " + current_access_token}
    r = requests.get('https://api.spotify.com/v1/me', headers=headers)
    rj = r.json()
    user_id = rj.get('id')
    return user_id


@app.route("/me/artists")
def get_me_artists():
    current_access_token = request.headers.get('AT')
    headers = {'Authorization': "Bearer " + current_access_token}
    r = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers)
    rj = r.json()
    items_arr = []
    items = rj.get('items')
    for item in items:
        curr = {'name': item.get('name'), 'img': item.get('images')[1].get('url'), 'genres': item.get('genres'),
                'id': item.get('id')}
        items_arr.append(curr)
    return items_arr


@app.route("/me/tracks")
def get_me_tracks():
    current_access_token = request.headers.get('AT')
    headers = {'Authorization': "Bearer " + current_access_token}
    r = requests.get('https://api.spotify.com/v1/me/top/tracks', headers=headers)
    rj = r.json()
    items_arr = []
    items = rj.get('items')
    for item in items:
        curr = {'artist': item.get('artists')[0].get('name'), 'name': item.get('name'),
                'img': item.get('album').get('images')[1].get('url'), 'id': item.get('id')}
        # Second Image 300x300
        items_arr.append(curr)
    return items_arr


@app.route("/me/recommendations")
def get_me_recommendations():
    current_access_token = request.headers.get('AT')
    headers = {'Authorization': "Bearer " + current_access_token}
    params = {'seed_artists': '4NHQUGzhtTLFvgF5SZesLK', 'seed_genres': 'country,pop,electropop',
              'seed_tracks': '0c6xIDDpzE81m2q797ordA'}
    r = requests.get('https://api.spotify.com/v1/recommendations', headers=headers, params=params)
    rj = r.json()
    items_arr = []
    items = rj.get('tracks')
    for item in items:
        # Second Image 300x300
        curr = {'artist': item.get('artists')[0].get('name'), 'name': item.get('name'),
                'img': item.get('album').get('images')[1].get('url'), 'id': item.get('id')}
        items_arr.append(curr)
    return items_arr
