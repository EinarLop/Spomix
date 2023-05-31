import requests


def get_me(current_access_token):
    headers = {'Authorization': "Bearer " + current_access_token}
    r = requests.get('https://api.spotify.com/v1/me', headers=headers)
    print("--------- helper function -----", r.text)
    
    rj = r.json()
    print("--------- helper function -----", rj)
    user_id = rj.get('id')
    return user_id
