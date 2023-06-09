import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import json


# Use a service account.

credents = {
  "type": "service_account",
  "project_id": "spomix-23189",
  "private_key_id": os.environ.get("private_key_id"),
  "private_key": os.environ.get("private_key").replace(r'\n', '\n'),
  "client_email": os.environ.get("client_email"),
  "client_id": os.environ.get("client_id_fb"),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": os.environ.get("client_x509_cert_url"),
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-i19gj%40spomix-23189.iam.gserviceaccount.com"
}

cred = credentials.Certificate(credents)

app = firebase_admin.initialize_app(cred)

db = firestore.client()
