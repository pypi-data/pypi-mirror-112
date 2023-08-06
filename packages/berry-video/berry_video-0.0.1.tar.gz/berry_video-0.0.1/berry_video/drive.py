import os


from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools


def get_cred(path):
    store_path = os.path.join(path, 'storage.json')
    store = file.Storage(store_path)
    creds = store.get()
    if not creds or creds.invalid:
        SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
        args = tools.argparser.parse_args(args=["--noauth_local_webserver"])
        secret_path = os.path.join(path, 'secret.json')
        flow = client.flow_from_clientsecrets(secret_path, SCOPES)
        creds = tools.run_flow(flow, store, args)
    return creds

def list_files(path):
    creds = get_cred(path)
    DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))
    return DRIVE.files().list().execute().get('files', [])