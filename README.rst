Backup files to Google Drive
============================

Files in the given folder ``'-p','--path'``  no older than one day are encrypted and uploaded to Google Drive.
Files larger than 1GB will be split. 
All file older then one day will be deletet on remote

Read the Google Drive API help. `Link <https://developers.google.com/drive/api/v3/quickstart/python>`_. and the Cryptography library. `Link <https://cryptography.io/en/latest/fernet/>`_

Install
----------
pip3 install -r requirements.txt

Use
---
``python3 drive.py [-h] [-p PATH] [--debug] [-b] [-d DOWNLOAD] [-l] [--delete]``

optional arguments:
  -h, --help                       Show this help message and exit
  -p PATH, --path PATH             Path in which the files to be backed up are located.
  --debug                          Debug mode
  -b, --backup                     Start backup
  -d <FileID>, --download <FileID> Download a single file with the given FileID
  -l, --list                       List remote files
  --delete                         Delete all remotefiles

