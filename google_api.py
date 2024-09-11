import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']


# Authenticate and initialize the Drive API client
def authenticate():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no valid credentials, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'data/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)


# Create a folder in Google Drive or retrieve its ID if it already exists
def create_or_get_folder(drive_service, folder_name):
    # Check if folder already exists
    query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])

    if items:
        # Folder already exists, return the ID
        print(f"Folder '{folder_name}' already exists.")
        return items[0]['id']
    else:
        # Create the folder and return its ID
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = drive_service.files().create(body=file_metadata, fields='id').execute()
        print(f"Folder '{folder_name}' created.")
        return folder.get('id')


# Check if a file with the same name already exists in the folder
def file_exists_in_drive(file_name, folder_id, drive_service):
    query = f"'{folder_id}' in parents and name = '{file_name}' and trashed = false"
    results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    return items[0]['id'] if items else None  # Return file ID if the file exists, None otherwise


# Delete the existing file in Google Drive
def delete_file(file_id, drive_service):
    try:
        drive_service.files().delete(fileId=file_id).execute()
        print(f"Deleted file with ID: {file_id}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Upload a file to Google Drive, replacing it if it already exists
def upload_file(file_path, folder_id, drive_service):
    file_name = os.path.basename(file_path)
    existing_file_id = file_exists_in_drive(file_name, folder_id, drive_service)

    # If the file exists, delete it before uploading the new one
    if existing_file_id:
        delete_file(existing_file_id, drive_service)

    # Upload the new file
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]  # Specify the folder to upload to
    }
    media = MediaFileUpload(file_path, resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Uploaded file '{file_path}' with file ID: {file.get('id')}' to folder ID: {folder_id}")


# Upload all files in the project folder to a specified folder in Google Drive
def upload_all_files_in_project_folder():
    drive_service = authenticate()

    # Specify the folder name
    folder_name = "graphicsCodeLab01"

    # Create or get the folder ID
    folder_id = create_or_get_folder(drive_service, folder_name)

    project_folder = os.getcwd()

    for root, dirs, files in os.walk(project_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # Skip files like google_api.py, token.pickle, and credentials.json
            if file_name not in ['google_api.py', 'token.pickle', 'credentials.json']:
                upload_file(file_path, folder_id, drive_service)


# Function to call in the main.py
def backup_to_drive():
    upload_all_files_in_project_folder()
