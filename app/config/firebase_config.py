import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

if not firebase_admin._apps:
    service_account_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")

    if service_account_json:
        service_account_dict = json.loads(service_account_json)
        cred = credentials.Certificate(service_account_dict)
    else:
        cred_path = "./app/config/ServiceAccountKey.json"
        cred = credentials.Certificate(cred_path)

    firebase_admin.initialize_app(cred)

db = firestore.client()