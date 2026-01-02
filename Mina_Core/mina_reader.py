import os.path
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    service = build('drive', 'v3', credentials=creds)

    print("\n--- MINA CORE: ĐANG TRUY XUẤT NỘI DUNG ---")

    # 1. Tìm file có tên 'Mina_Setup.md'
    results = service.files().list(
        q="name = 'Mina_Setup.md' and trashed = false",
        fields="files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print("⚠️ Không tìm thấy file Mina_Setup.md trên Drive.")
    else:
        file_id = items[0]['id']
        file_name = items[0]['name']
        print(f"📖 Đang đọc file: {file_name} (ID: {file_id})")

        # 2. Tải và đọc nội dung file
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        
        # 3. Hiển thị nội dung ra màn hình
        content = fh.getvalue().decode('utf-8')
        print("\n--- NỘI DUNG FILE ---")
        print(content)
        print("---------------------")

if __name__ == '__main__':
    main()