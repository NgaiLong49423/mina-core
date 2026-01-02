# Mina_Core – Python Core for Mina

> Ghi chú cho chính bạn (Gia Long) khi quay lại dự án.

## 1. Thư mục này là gì?

Mina_Core là **core Python package** dùng để:
- Kết nối Google Drive để đọc các file nhân cách (`*_Setup.md`).
- Khởi động các module:
  - `mina_drive.py` – kiểm tra thư mục MINA_SYSTEM_DATABASE trên Drive.
  - `mina_reader.py` – đọc một file setup cụ thể (ví dụ Mina_Setup.md).
  - `mina_system.py` – khởi động hệ thống nhân cách (Mina/Mila/Misa/Mita) dùng Gemini.
- Đóng vai "bộ não kỹ thuật" phía sau các agent khác.

Cấu trúc chính:
- `drive_auth.py` – xử lý OAuth Google Drive, tạo `drive service` dùng chung.
- `mina_drive.py` – test kết nối và liệt kê file trong thư mục MINA_SYSTEM_DATABASE.
- `mina_reader.py` – đọc nội dung file setup trên Drive và in ra.
- `mina_system.py` – chọn nhân cách, nạp setup, tạo cuộc hội thoại với Gemini.

## 2. Chuẩn bị trước khi chạy

### 2.1. Python & thư viện

- Python >= 3.10
- Cài dependency từ file requirements ở gốc dự án:

```bash
pip install -r requirements.txt
```

Các gói chính:
- `google-api-python-client`, `google-auth-oauthlib`, `google-auth-httplib2` – dùng cho Google Drive.
- `google-generativeai` – dùng cho Gemini.

### 2.2. Google Drive credentials (secrets)

Mina_Core KHÔNG còn lưu secrets cứng trong repo. Bạn cần tự chuẩn bị:
- `credentials.json` – file client từ Google Cloud Console (OAuth Client ID).
- `token.json` – file token sau lần auth đầu tiên (sẽ được tạo tự động).

Có 2 cách đặt thư mục chứa các file này:

**Cách 1 – Mặc định (đơn giản):**
- Tạo thư mục `secrets` cạnh thư mục [Mina_Core](.).
- Bỏ `credentials.json` vào đó.
- Lần chạy đầu tiên, hệ thống sẽ tạo `token.json` trong cùng thư mục.

**Cách 2 – Thư mục riêng (an toàn hơn):**
- Tạo một thư mục bên ngoài repo, ví dụ:
  - `D:\Mina_Secrets`
- Bỏ `credentials.json` (và nếu có thì cả `token.json`) vào đó.
- Đặt biến môi trường:
  - `MINA_SECRETS_DIR = D:\Mina_Secrets`
- Module `drive_auth.py` sẽ tự động đọc đường dẫn này.

Nếu thiếu `credentials.json`, Mina_Core sẽ báo lỗi với đường dẫn nó đang dùng để bạn kiểm tra.

### 2.3. Gemini API key

Trong [mina_system.py](mina_system.py), Mina Core đọc API key từ biến môi trường:
- Tên biến: `GEMINI_API_KEY`

Bạn cần:
- Lấy API key từ Google AI Studio / Generative AI.
- Đặt biến môi trường trên Windows, ví dụ:
  - `GEMINI_API_KEY = YOUR_KEY_HERE`

Không hard-code key vào file Python.

## 3. Cách chạy các module chính

Tất cả ví dụ dưới đây giả sử bạn đang đứng ở thư mục gốc `mina-core/`.

### 3.1. Kiểm tra kết nối Drive

Liệt kê thư mục MINA_SYSTEM_DATABASE trên Google Drive:

```bash
python -m Mina_Core.mina_drive
```

### 3.2. Đọc file setup (ví dụ Mina_Setup.md)

```bash
python -m Mina_Core.mina_reader
```

Module này sẽ:
- Tìm file `Mina_Setup.md` trên Drive.
- Tải nội dung và in ra console.

### 3.3. Khởi động hệ thống nhân cách (Mina/Mila/Misa/Mita)

```bash
python -m Mina_Core.mina_system
```

Luồng chính:
- Kết nối Drive qua `get_drive_service()`.
- Tìm các file có tên kiểu `*_Setup.md` (Mina_Setup, Mila_Setup, Misa_Setup, Mita_Setup...).
- Cho bạn chọn nhân cách.
- Đọc nội dung setup tương ứng.
- Tạo một phiên chat với Gemini (model `gemini-1.5-flash`).
- Bạn gõ message → hệ thống trả lời dưới vai nhân cách đã chọn.

Thoát vòng lặp chat bằng cách gõ `exit` hoặc `quit`.

## 4. Biến môi trường quan trọng (tóm tắt)

- `MINA_SECRETS_DIR` – (tùy chọn) thư mục chứa `credentials.json` và `token.json`.
  - Nếu không đặt, mặc định dùng `Mina_Core/secrets`.
- `GEMINI_API_KEY` – bắt buộc để dùng `mina_system.py`.

## 5. Ghi chú cho bản thân

- Repo hiện tại đang là **private**, dùng để học và build MVP, nên cách tổ chức như trên là ổn.
- Khi (và chỉ khi) muốn public:
  - Đảm bảo không có file secrets thật nằm trong repo.
  - Giữ cách dùng biến môi trường như hiện tại.
  - Có thể thêm file `.env.example` để hướng dẫn người khác tự điền key.

> Nếu sau này quay lại mà quên flow, chỉ cần:
> 1. Đọc lại file này.
> 2. Kiểm tra biến môi trường.
> 3. Chạy `python -m Mina_Core.mina_system` để đánh thức một nhân cách.
