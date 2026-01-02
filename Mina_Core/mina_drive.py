import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Quyền truy cập: Chỉ đọc file
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def main():
    creds = None
    # File token.json lưu trữ quyền đăng nhập sau lần đầu tiên
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Tìm file credentials.json bạn vừa bỏ vào thư mục
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    print("--- ĐANG KẾT NỐI VỚI HỆ THỐNG MINA ---")
    
    # BƯỚC 1: Tìm ID của thư mục [MINA_SYSTEM_DATABASE]
    query_folder = "name = '[MINA_SYSTEM_DATABASE]' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    folder_results = service.files().list(q=query_folder, fields="files(id, name)").execute()
    folders = folder_results.get('files', [])

    if not folders:
        print("⚠️ Không tìm thấy thư mục [MINA_SYSTEM_DATABASE] trên Drive của bạn.")
        return

    folder_id = folders[0]['id']
    print(f"✅ Đã kết nối tới thư mục gốc. (ID: {folder_id})")

    # BƯỚC 2: Liệt kê các file trong đó (bao gồm cả thư mục con như 01_System_Setup)
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed = false",
        fields="files(id, name, mimeType)").execute()
    items = results.get('files', [])

    if not items:
        print('Thư mục đang trống.')
    else:
        print('\nCác tệp tin hệ thống tìm thấy:')
        for item in items:
            print(f"- {item['name']} ({item['mimeType']})")

if __name__ == '__main__':
    main()