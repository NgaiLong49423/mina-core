"""Liệt kê thư mục MINA_SYSTEM_DATABASE trên Google Drive.

Sử dụng helper chung get_drive_service trong drive_auth để xử lý
OAuth và đảm bảo credentials/token chỉ nằm trong thư mục secrets/.
"""

try:
    # Khi chạy dưới dạng package: python -m Mina_Core.mina_drive
    from .drive_auth import get_drive_service
except ImportError:  # fallback khi chạy trực tiếp trong thư mục Mina_Core
    from drive_auth import get_drive_service  # type: ignore


def main():
    service = get_drive_service()

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