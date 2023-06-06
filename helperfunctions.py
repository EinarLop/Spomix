import requests


def get_me(current_access_token):
    headers = {'Authorization': "Bearer " + current_access_token}
    r = requests.get('https://api.spotify.com/v1/me', headers=headers)  
    print("Helper", r.text)  
    rj = r.json()
    
    user_id = rj.get('id')
    return user_id

def get_me_full(current_access_token, user_id):
    headers = {'Authorization': "Bearer " + current_access_token}
    r = requests.get(f'https://api.spotify.com/v1/users/{user_id}', headers=headers)    
    rj = r.json()
    print(rj, "skjksjks")
    if rj.get("error"):
        return None
    return rj
