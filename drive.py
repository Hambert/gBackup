# filehandling
import os.path
import pathlib 

# Google API
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload
import io
from apiclient.http import MediaIoBaseDownload

# filezize
from hurry.filesize import size

# script arguments
import argparse

# logging
import logging

from datetime import datetime

# Eigene
from modules import myCrypto2
from modules import myFile
from modules import mySearch
from modules import mySplitFile

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', "https://www.googleapis.com/auth/drive.file",
          "https://www.googleapis.com/auth/drive"]


def main(args):

    key = b'uoF-sow9hAnkavYnOb0QbMTNJ2KAc6vQPL_4rizDI4Y='
    ignoreFiles = [".DS_Store"]
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):

        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if os.path.exists('credentials.json'):

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

    else:
        debug.error('no credentials.json found')
        print('login to google developer and create a credentials.json file')
        return

    service = build('drive', 'v3', cache_discovery=False, credentials=creds)

    # listFiles(service)
    # uploadFile(service)
    # listFiles(service)
    # serarchFile(testfiles)

    # Liste aus datei lesen
    if args.path != None:
        if args.all != None:
            actualFiles = mySearch.serarchFile(args.path)
        else:
            fileList = os.listdir(args.path)
            actualFiles = []
            for file in fileList:
                actualFiles.append([file, os.path.getmtime(args.path + "/" + file) ])

        if args.debug and actualFiles:
            print('local files:')
            print(actualFiles)

    if args.list:
        onlineFilelist = listFiles(service)
        if not onlineFilelist:
            print("Remote Verzeichnis ist leer")
        else:
            print("Remote Verzeichnis:")
            for item in onlineFilelist:
                print(item)

    
    if args.backup:
        if args.path != None:
            logging.debug("Start Backup")

            onlineFilelist = listFiles(service)
            print(onlineFilelist)

            uploadFileList = []

            if actualFiles is not None:
                print(10 * "#")
                # iteriert jede Datei im lokalem Verzeichnis und 
                # prüft, ob diese in der online Liste enthalten ist.
                for file in actualFiles:

                    print("is " + file[0] + " online?")
                    fileFound = False

                    if onlineFilelist is not None:
                        print(10 * "#")
                        for onFile in onlineFilelist:

                            if file[0] in onFile['name']:
                                # onlineFilelist.remove(onFile)
                                print('match: ' + file[0])
                                fileFound = True
                            else:
                                print('no match: ' + onFile['name'])

                        # Liste mit nicht online gefundenen Dateien
                        # Lösche file[0] aus der Liste
                        onlineFilelist = list(filter(lambda x: file[0] not in x['name'], onlineFilelist))

                    if fileFound:
                        continue
                    else:
                        uploadFileList.append(file[0])
                        print('Add File for upload: ' + file[0] )
            else:
                print("no local files found")

            print(10 * "#" + " start deleting files")
            print(onlineFilelist)
            if onlineFilelist is not None:
                for delFile in onlineFilelist:
                    try:
                        deleteFile(service, delFile['id'])
                        print('Datei gelöscht: ' + str(delFile))
                    except:
                        print("Fehler beim löschen der Datei: " + str(delFile) )
            else:
                print("no files online")

            for file in uploadFileList:
                # upload all file in list
                if os.path.getsize(args.path + '/' + file) > 1000000000:

                    print('file must be ' + file + ' split')
                    parts = mySplitFile.split(args.path + '/', file, 1000000000)
                    for i in range(1, parts + 1):
                        tFile = file + '.part%04d' % i

                        print('file: ' + tFile + ' encrypt')
                        myCrypto2.encrypt_file(args.path + '/' + tFile, key)
                        print('file: ' + tFile + '.enc upload')
                        uploadFileChunkMode(service, args.path + '/', tFile + ".enc")
                        print('file: ' + tFile + '.enc delete')
                        os.remove(args.path + '/' + tFile + ".enc")
                        print('file: ' + tFile + ' delete')
                        os.remove(args.path + '/' + tFile)

                else:
                    print('file: ' + file + ' encrypt')
                    myCrypto2.encrypt_file(args.path + '/' + file, key)
                    print('file: ' + file + '.enc upload')
                    uploadFileChunkMode(service, args.path + '/', file + ".enc")
                    os.remove(args.path + '/' + file + ".enc")
        else:
            print('no path is given')
            logging.info("no path is given")

    elif args.delete:
        onlineFilelist = listFiles(service)

        if onlineFilelist is not None:
            for delFile in onlineFilelist:
                try:
                    deleteFile(service, delFile['id'])
                    print('Datei gelöscht: ' + str(delFile))
                except:
                    print("Fehler beim löschen der Datei: " + str(delFile) )

    elif args.download != None:
        
        if args.path == None:
            logging.error("no given path")
            print("Parameter path is missing")
        else:
            logging.debug("Download the file %s" % args.download)
            print("Download the file %s" % args.download)
            fileName = downloadFile(lc_service = service,fileID = args.download,path = args.path )
            if fileName is not None and fileName[-3:] == 'enc':
                myCrypto2.decrypt_file( args.path + "/" + fileName, args.path + "/" + fileName[:-4], key)
                os.remove(args.path + "/" + fileName)


def listFiles(lc_service):
    # Call the Drive v3 API
    results = lc_service.files().list(
        pageSize=100, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if items:
        myFile.write_to_file(items, "filelist.json")
        return items


def uploadFile(lc_service, path, fileName=None):
    # Call the Drive v3 API

    file_metadata = {'name': fileName}
    media = MediaFileUpload(path + fileName,
                            mimetype='*/*')
    file = lc_service.files().create(body=file_metadata,
                                     media_body=media,
                                     fields='id').execute()
    fileID = file.get('id')
    print('File ID: %s' % id)
    return fileID


def deleteFile(lc_service, fileID):
    response = lc_service.files().delete(fileId=fileID).execute()
    if response == '':
        return None
    else:
        return response


def uploadFileChunkMode(lc_service, path, fileName=None):
    CHUNK_SIZE = 256 * 1024
    DEFAULT_CHUNK_SIZE = 100 * 1024 * 1024

    media = MediaFileUpload(path + fileName, resumable=True, chunksize=CHUNK_SIZE)

    file_metadata = {'name': fileName}

    res = lc_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    )

    response = None
    while response is None:
        status, response = res.next_chunk()
        try:
            if status.total_size > 1000:
                print(str(size(status.resumable_progress)) + '/' + str(size(status.total_size)) + ' Bytes transfered')
        except:
            pass

    if response == '':
        print(response)
        return None
    else:
        print(response)
        return response

def downloadFile(lc_service, fileID, path):
    """
    Download a file

    Attributes
    ----------
    lc_service : googleapiclient.discovery
        the google drive api client
    fileID : str
        the file ID

    return
    fileName : str
     """
    file = lc_service.files().get(fileId=fileID).execute()
    fileName = file['name'].replace(" ","_").replace("\n","")

    request = lc_service.files().get_media(fileId=fileID)
    fullPath = path + os.path.sep + fileName

    fh = io.FileIO( fullPath, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    try:
        while done is False:
            status, done = downloader.next_chunk()
            print ("Download %d%%." % int(status.progress() * 100))

        return fileName

    except Exception as e:
        print("Konnte datei nicht herunterladen")
        print(e)
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This is a backup tool for Google Drive')
    parser.add_argument('-p', '--path', help='Path in which the files to be backed up are located.')
    parser.add_argument('-a', '--all', help='Backup all files')
    parser.add_argument('--debug', help='Debug mode', action='store_true')
    parser.add_argument('-b','--backup', help='start backup', action='store_true')
    parser.add_argument('-d','--download', help='Download a single file with the given FileID')
    parser.add_argument('-l', '--list', help='list remote files', action='store_true')
    parser.add_argument('--delete', help='delete all remotefiles', action='store_true')
    args = parser.parse_args()

    print("Pfad: %s" % args.path)

    
    
    # set the debug level
    if args.debug:
      loglevel = logging.DEBUG
    else:
      loglevel = logging.INFO

    print("Debuglevel: "+ str( loglevel ))

    # Date for log file
    n = datetime.now()

    # logging
    logging = logging
    logging.basicConfig(
        filename = n.strftime("%Y-%m-%d") +'_gBackup.log',
        format='%(asctime)s - %(levelname)s:%(message)s',
        filemode='a',
        level=loglevel)

    logging.debug("loggin init")

    main(args)

    logging.debug("script finished")
