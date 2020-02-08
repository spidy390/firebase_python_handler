import os
import datetime
import firebase_admin
from firebase_admin import credentials, firestore, storage
from credentials import CERTIFICATE_PATH,STORAGE_PATH

def parsetext(file_path):
    data = {}
    with open(file_path, 'r') as f:
        for line in f:
            key, value = line.split(' : ')
            if key.lower() in data:
                data[key.lower()] += '\n' + value.rstrip()
            else:
                data[key.lower()] = value.rstrip()
    return data

# Use a service account
cred = credentials.Certificate(CERTIFICATE_PATH)
app = firebase_admin.initialize_app(cred, {'storageBucket': STORAGE_PATH})

db = firestore.client()
bucket = storage.bucket(app=app)

for files in os.listdir('files/'):
    if files.endswith('.txt'):
        data = parsetext('files/'+files)
        name = files.replace('.txt', '')
        doc_ref = db.collection('hediyeler').document(name)
        doc_ref.set(data)
    if files.endswith('.jpeg'):
        outfile=os.getcwd()+'/files/'+files
        blob = bucket.blob(files)
        with open(outfile, 'rb') as my_file:
            blob.upload_from_file(my_file)

# for printing uploaded file use the followibg lines. It will give u a link to see data
#blob = bucket.blob("car.jpeg")
#print(blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET'))