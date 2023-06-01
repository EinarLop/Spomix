from firebaseconfig import *
import helperfunctions 

def create_group(group_name, user_id):
    doc_ref = db.collection(u'groups')
    response = doc_ref.add({
        u'name': group_name,
        u'members': [user_id],
    })
    group_id = response[1].id
    return group_id


def join_group(group_id, user_id):
    doc_ref = db.collection(u'groups').document(group_id)
    doc_snapshot = doc_ref.get()
    if doc_snapshot.exists:
        doc_ref.update({
            u'members': firestore.ArrayUnion([user_id])
        })
        return True
    return False

def set_user(user_id: str,  refresh_token: str):
    doc_ref = db.collection(u'users').document(user_id)
    doc_ref.set({
        u'refresh_token': refresh_token,
        u'artists': [],
        u'tracks': [],
        u'genres': []
    })


def get_user_token(user_id):
    doc_ref = db.collection(u'users').document(user_id)
    doc_snapshot = doc_ref.get()
    if doc_snapshot.exists:
        doc_data = doc_snapshot.to_dict()
        print("Document data: {}".format(doc_data))
    else:
        print("Document {} does not exist!".format(user_id))


    
def update_user_artists(user_id, artists, genres):
    doc_ref = db.collection(u'users').document(user_id)
    doc_snapshot = doc_ref.get()
    
    if doc_snapshot.exists:
        response = doc_ref.update({
            u'artists': artists,
            u'genres': genres
        })
        print("update_user_artists", response)

def update_user_tracks(user_id, tracks):
    doc_ref = db.collection(u'users').document(user_id)
    doc_snapshot = doc_ref.get()
    
    if doc_snapshot.exists:
        response = doc_ref.update({
            u'tracks': tracks,
        })
        print("update_user_artists", response)

def get_group_seeds(group_id):
    group_tracks = []
    group_artists = []
    group_genres = []
    doc_ref = db.collection(u'groups').document(group_id)
    doc_snapshot = doc_ref.get()
    if doc_snapshot.exists:
        doc_data = doc_snapshot.to_dict()
        group_members = doc_data["members"]
        for member in group_members:
            user_ref = db.collection(u'users').document(member)
            user_snapshot = user_ref.get()
            if user_snapshot.exists:
                user_data = user_snapshot.to_dict()
                group_tracks += user_data["tracks"]
                group_artists += user_data["artists"]
                group_genres += user_data["genres"]
                print(len(group_tracks), len(group_artists), len(group_genres), user_data)
        return group_tracks, group_artists, group_genres

    else:
        print("Document {} does not exist!".format(group_id))
        return None


def get_group(group_id, access_token):
    doc_ref = db.collection(u'groups').document(group_id)
    
    doc_snapshot = doc_ref.get()
    if doc_snapshot.exists: 
         doc_data = doc_snapshot.to_dict()
         members = doc_data.get("members")
         profiles = []
         if members:
             for member in members:
                current_member = helperfunctions.get_me_full(access_token, member)
                if current_member:
                    profiles.append(current_member)
         doc_data["profiles"] = profiles
         return doc_data
    return None


