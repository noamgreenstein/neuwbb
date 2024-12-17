from googleapiclient.discovery import build
from google.oauth2 import service_account


class DocCreator:
    def __init__(self):
        self.scopes = [
            'https://www.googleapis.com/auth/documents',
            'https://www.googleapis.com/auth/drive'  # Added Drive scope for sharing
        ]
        self.file = '/Users/noamgreenstein/Documents/Projects/NEUWBB24/neuwbb-4a7d2a9d8c8e.json'
        self.credentials = service_account.Credentials.from_service_account_file(
            self.file, scopes=self.scopes)
        self.docs_service = build('docs', 'v1', credentials=self.credentials)
        self.drive_service = build('drive', 'v3', credentials=self.credentials)
        self.email = "ngreenstein3@gmail.com"
        self.template = '1z7RUl_h0UPIAB_O2EIZT4I9dsPPQglrw1XlTmO2PuvY'

    def create_doc(self, title, requests):
        new_file = self.drive_service.files().copy(
            fileId=self.template,
            body={
                'name': title}
        ).execute()
        document_id = new_file.get('id')

        self.drive_service.permissions().create(
            fileId=document_id,
            body={
                'type': 'user',
                'role': 'writer',
                'emailAddress': self.email
            },
            sendNotificationEmail=False
        ).execute()

        self.docs_service.documents().batchUpdate(
            documentId=document_id,
            body={'requests': requests}
        ).execute()

        return f'https://docs.google.com/document/d/{document_id}'



