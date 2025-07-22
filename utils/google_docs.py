import os
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
]


def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def get_drive_service():
    creds = get_credentials()
    return build("drive", "v3", credentials=creds)


def get_docs_service():
    creds = get_credentials()
    return build("docs", "v1", credentials=creds)


def get_or_create_folder(folder_name):
    drive_service = get_drive_service()

    # Search for folder by name
    query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    results = (
        drive_service.files()
        .list(q=query, spaces="drive", fields="files(id, name)")
        .execute()
    )
    files = results.get("files", [])

    if files:
        return files[0]["id"]

    # Create folder if it doesn't exist
    file_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    folder = drive_service.files().create(body=file_metadata, fields="id").execute()
    return folder["id"]


def create_doc_in_folder(folder_name, title=None):
    docs_service = get_docs_service()
    drive_service = get_drive_service()

    if title is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        title = f"WWR Job Feed - {timestamp}"

    # Create the document
    doc = docs_service.documents().create(body={"title": title}).execute()
    doc_id = doc["documentId"]

    # Move it to the folder
    folder_id = get_or_create_folder(folder_name)
    drive_service.files().update(
        fileId=doc_id, addParents=folder_id, removeParents="root", fields="id, parents"
    ).execute()

    return doc_id


def append_to_doc(document_id, text):
    docs_service = get_docs_service()
    requests = [{"insertText": {"location": {"index": 1}, "text": text}}]
    docs_service.documents().batchUpdate(
        documentId=document_id, body={"requests": requests}
    ).execute()
