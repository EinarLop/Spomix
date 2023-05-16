from firebaseconfig import *


def create_group(group_name, user_id):
    doc_ref = db.collection(u'groups')
    response = doc_ref.add({
        u'name': group_name,
        u'members': [user_id],
    })
    print("Group Id",response[1].id)


def join_group(group_id, user_id):
    doc_ref = db.collection(u'groups').document(group_id)
    response = doc_ref.update({
        u'members': firestore.ArrayUnion([user_id])
    })
    print(response)






def set_user(user_id: str,  refresh_token: str):
    doc_ref = db.collection(u'users').document(user_id)
    doc_ref.set({
        u'refresh_token': refresh_token
    })


def get_user_token(user_id):
    doc_ref = db.collection(u'users').document(user_id)
    doc_snapshot = doc_ref.get()
    if doc_snapshot.exists:
        doc_data = doc_snapshot.to_dict()
        print("Document data: {}".format(doc_data))
    else:
        print("Document {} does not exist!".format(user_id))
