import datetime
from flask import Flask, render_template
import pickle
import os.path
import io
from httplib2 import Http
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from apiclient import errors
import pandas as pd

from google.cloud import storage



app = Flask(__name__)

# buckets functions
def list_buckets():
    """Lists all buckets."""

    storage_client = storage.Client()
    buckets = storage_client.list_buckets()

    for bucket in buckets:
        print(bucket.name)

def upload_blob(source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    bucket_name = "visualisation-jbu.appspot.com"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_file(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

# Google drive functions
SCOPES = ['https://www.googleapis.com/auth/drive', 
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive.metadata.readonly']

def get_gdrive_access():
  """
  Gets access to google drive
  """
  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.pickle'):
      with open('token.pickle', 'rb') as token:
          creds = pickle.load(token)

  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'keys/client_id_desktop.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
 
  service = build('drive', 'v3', credentials=creds)
  return service

def get_folder_id(service, folder_name):
    # query to get the shared folder with data
    query="sharedWithMe and name contains '%s'" % (folder_name)
    response = service.files().list(q= query, spaces='drive',
                                        fields='nextPageToken, files(id, name)').execute()
    results = response.get('files', [])
    if results:
      folder_id = results[0].get("id")
      return folder_id
    else:
      return None

def get_files(service, folder_id):

  # get the existing files
  existing_files = get_existing_files()

  # query to get the shared folder with data
  query="'%s' in parents" % (folder_id)
  response = service.files().list(q= query, spaces='drive',
                                  fields='nextPageToken, files(id, name)').execute()
  results = response.get('files', [])

  new_files_added = []
  for result in results:
    file_name = str(result.get("name"))

    if file_name not in existing_files:
      print("Need to download %s " % file_name)
      request = service.files().get_media(fileId=result.get("id"))
      fh = io.BytesIO()
      downloader = MediaIoBaseDownload(fh, request)
      done = False
      while done is False:
          status, done = downloader.next_chunk()
          print("Download %s %d%%." % (file_name, int(status.progress() * 100)))

      fh.seek(0)
      upload_blob(fh, file_name)
      new_files_added.append(file_name)

  return new_files_added

def get_existing_files():

  # for bucket list 
  storage_client = storage.Client()
  blobs = storage_client.list_blobs("visualisation-jbu.appspot.com", delimiter="/")

  filenames = []
  for blob in blobs:
     filenames.append(blob.name)

  return filenames
  # for localhost
  # return [f for f in os.listdir("../saved_data/") if ".tsv" in f]

def process_files(file_paths):
  raw_dfs = {}
  for file_path in file_paths:
    file_name = file_path.split("/")[-1].split()[0]
    raw_dfs[file_name] = pd.read_csv(file_path, sep='\t') 
  
  return raw_dfs

@app.route('/')
def root():

    drive_service = get_gdrive_access()
 
    # list_buckets()

    folder_id = get_folder_id(drive_service, "test_folder")
    files_added = []
    if folder_id != None:
        # donwload the files
        print("folder id", folder_id)
        files_added = get_files(drive_service, folder_id)

    return render_template('index.html', times=files_added)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)