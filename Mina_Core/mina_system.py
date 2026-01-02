import os
# CHẶN LOG NHIỄU: Thêm 2 dòng này đầu tiên
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'

import io
import google.generativeai as genai
from googleapiclient.http import MediaIoBaseDownload

try:
    # Khi chạy dưới dạng package: python -m Mina_Core.mina_system
    from .drive_auth import get_drive_service
except ImportError:  # fallback khi chạy trực tiếp trong thư mục Mina_Core
    from drive_auth import get_drive_service  # type: ignore

# 1. Cấu hình AI (đọc API key từ biến môi trường, không hard-code)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise RuntimeError(
        "Thiếu biến môi trường GEMINI_API_KEY. Hãy đặt key trước khi chạy Mina Core."
    )

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def read_file_content(service, file_id):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return fh.getvalue().decode('utf-8')

def main():
    try:
        service = get_drive_service()
        print("\n--- MINA CORE: ĐANG KHỞI ĐỘNG ---")
        
        query = "name contains '_Setup.md' and trashed = false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        personas = results.get('files', [])

        if not personas:
            print("⚠️ Không tìm thấy file nhân cách!")
            return

        print("\nChọn nhân cách bạn muốn đánh thức:")
        for i, p in enumerate(personas):
            print(f"{i+1}. {p['name'].replace('_Setup.md', '')}")

        choice = int(input("\nNhập số: ")) - 1
        selected = personas[choice]
        
        print(f"🚀 Đang nạp {selected['name']}...")
        instruction = read_file_content(service, selected['id'])
        
        chat = model.start_chat(history=[])
        chat.send_message(f"Hệ thống: Hãy đóng vai nhân cách này: {instruction}")
        
        name = selected['name'].split('_')[0]
        print(f"\n--- {name.upper()} ĐÃ SẴN SÀNG ---")
        
        while True:
            msg = input("Bạn: ")
            if msg.lower() in ['exit', 'quit']: break
            
            response = chat.send_message(msg)
            print(f"\n{name}: {response.text}\n")
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == '__main__':
    main()
    