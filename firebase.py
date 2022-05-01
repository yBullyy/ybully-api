import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

cred = credentials.Certificate("cred.json")
firebase_admin.initialize_app(cred,{"storageBucket":"ybullyy.appspot.com"})


db = firestore.client()
bucket = storage.bucket() 
models_ref = db.collection(u'models')


def get_last_model() -> dict:
    doc = models_ref.order_by(u'date', direction=firestore.Query.DESCENDING).limit(1).get()
    data = doc[0].to_dict()
    return data

def add_model():
    last_version = int(get_last_model()['version'])
    curr_version = last_version + 1
    model_name = f'model_{curr_version}'
    data = {
        u'name': model_name,
        'version': curr_version,
        'date': firestore.SERVER_TIMESTAMP,
        'status': 'Retraining Requested'
    }
    models_ref.document(str(curr_version)).set(data)
    return curr_version


def update_model(model_version,data):
    models_ref.document(str(model_version)).update(data)


def upload_model(model_path:str):
    model_name = os.path.basename(model_path)
    blob = bucket.blob(model_name)
    blob.upload_from_filename(model_path)
    return model_name