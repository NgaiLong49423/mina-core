Quickstart — Mina Core (Phiên bản tiếng Việt)

Hướng dẫn nhanh này chỉ dẫn cách chạy backend tối giản trên Windows PowerShell.

1) Tạo và kích hoạt môi trường ảo (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Nếu PowerShell chặn việc chạy script, bạn có thể chạy (một lần, với quyền Admin):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

2) Cài đặt phụ thuộc (hiện tại không có gói bên thứ ba bắt buộc):

```powershell
pip install -r requirements.txt
```

3) Khởi động server HTTP nhỏ để kiểm tra (health):

```powershell
python backend\main.py --serve --port 8000
```

4) Kiểm tra bằng trình duyệt hoặc `curl`:

- http://localhost:8000/        -> trả về chuỗi văn bản (greeting)
- http://localhost:8000/health -> trả về JSON {"status":"ok"}

Ví dụ dùng `curl` trên PowerShell:

```powershell
curl http://localhost:8000/health
```

Ghi chú và lời khuyên:
- Hiện tại dự án dùng thư viện chuẩn của Python, nên `requirements.txt` để trống hoặc để ghi chú.
- Sử dụng môi trường ảo giúp tách biệt phụ thuộc khi bạn thêm thư viện sau này.

Những bước tiếp theo bạn có thể làm (tùy chọn):
- Mở rộng `memory/README.md` bằng ví dụ và API minimal (gợi ý cho module memory).
- Viết một test nhỏ để gọi `/health` tự động (pytest hoặc script đơn giản).
- Thêm Dockerfile để chạy server trong container (nếu muốn học Docker sau).

Bạn muốn tôi làm bước nào tiếp theo? (ví dụ: dịch `README.md` chính, viết `memory/README.md`, hoặc tạo test `/health`).