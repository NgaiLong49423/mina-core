import io
from googleapiclient.http import MediaIoBaseDownload
try:
    # Khi chạy dưới dạng package: python -m Mina_Core.mina_reader
    from .drive_auth import get_drive_service
except ImportError:  # fallback khi chạy trực tiếp trong thư mục Mina_Core
    from drive_auth import get_drive_service  # type: ignore


def main():
    service = get_drive_service()

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