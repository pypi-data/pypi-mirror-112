import json
from libvmake.utils import get_global_config, md5sum, private, get_gist_token, get_google_drive_config, get_default_encrypter
import os
import sys

try:
    from googleapiclient.discovery import build, Resource, MediaFileUpload
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.http import MediaIoBaseDownload
except ModuleNotFoundError:
    os.system(f'{sys.executable} -m pip install --no-input google-api-python-client google-auth-httplib2 google-auth-oauthlib')
    from googleapiclient.discovery import build, Resource, MediaFileUpload
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.http import MediaIoBaseDownload

google_drive_service = None

def init_googledrive_service(client_config: dict) -> Resource:

    name = md5sum(json.dumps(client_config))
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None

    token_file = os.path.join(os.path.expanduser("~"), '.libvmake', 'auth', f'{name}.token')

    defaultEncrypter = get_default_encrypter()
    if os.path.exists(token_file):
        with open(token_file, mode='rb') as f:
            token_file_content = defaultEncrypter.decrypt(f.read())
            user_info = json.loads(json.loads(token_file_content))
            creds = Credentials.from_authorized_user_info(user_info, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_local_server(port=0)
        os.makedirs(os.path.dirname(token_file), exist_ok=True)
        with open(token_file, 'wb') as f:
            f.write(defaultEncrypter.encrypt(json.dumps(creds.to_json())))

    service = build('drive', 'v3', credentials=creds)
    return service

@private
def init_googledrive_service_ex()->Resource:
    from libvmake import libvmake
    gist_token = get_gist_token()
    google_drive_config = get_google_drive_config()
    client_config = json.loads(libvmake.get_github_gist(gist_token, google_drive_config['gist_id'], google_drive_config['gist_file']))
    return init_googledrive_service(client_config)


def get_googledrive_service():
    global google_drive_service
    if google_drive_service is None:
        google_drive_service = init_googledrive_service_ex()
    return google_drive_service 

# return dict has name and id key
def lists(service: Resource) -> list:

    page_token = None
    items = []
    while True:
        results = service.files().list(
            pageSize=100, fields="nextPageToken, files(id, name)",
            pageToken=page_token).execute()
        items.extend(results.get('files', []))
        page_token = results.get('nextPageToken', None)
        if page_token is None:
            break
    return items


def upload(service: Resource, file: str, name: str = None, directory_ids: list = None, mimetype="application/octet-stream") -> str:
    media = MediaFileUpload(file, mimetype=mimetype)
    file = service.files().create(body={"parents": directory_ids, "name": name if name is not None else os.path.basename(file)},
                                  media_body=media,
                                  fields='id').execute()
    return file.get('id')


def mkdir(service: Resource, directory: str):
    file_metadata = {
        'name': directory,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata,
                                  fields='id').execute()
    return file.get('id')


def download(service: Resource, file_id, destfile) -> bool:
    request = service.files().get_media(fileId=file_id)
    done = False
    with open(destfile, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}")
        else:
            done = True
    return done


def find(service: Resource, name) -> list:
    page_token = None
    items = []
    while True:
        response = service.files().list(q=f"name = '{name}'",
                                        spaces='drive',
                                        fields='nextPageToken, files(id, name)',
                                        pageToken=page_token).execute()
        items.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return items


def delete(service: Resource, file_id: str):
    file = service.files().delete(fileId=file_id).execute()
    return file
