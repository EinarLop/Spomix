import requests


def get_me(current_access_token):
    headers = {'Authorization': "Bearer " + current_access_token}
    r = requests.get('https://api.spotify.com/v1/me', headers=headers)
    rj = r.json()
    user_id = rj.get('id')
    return user_id
