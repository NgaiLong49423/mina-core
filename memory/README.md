Memory  Lưu trữ reasoning, feedback và lịch sử

Tài liệu này mô tả mục đích, schema dữ liệu, ví dụ và cách sử dụng module Memory trong Mina.

## 1. Mục đích

- Lưu lại các proposal/luồng suy luận từ các agent (Mina, Mila, Misa, Mita, ...).
- Ghi provenance (ai nói gì, khi nào, với những giả định nào).
- Lưu feedback của người dùng và điểm đánh giá (reasoning score).
- Là nguồn để audit, debug, và huấn luyện/tuning sau này.

## 2. Nguyên tắc thiết kế

- Mỗi entry phải có provenance và timestamp.
- Dữ liệu readable (text) để dễ audit.
- Hỗ trợ truy vấn theo `session_id`, `user_id`, `agent_id`, `time range`.
- Hạn chế lưu secrets; nếu cần, lưu dưới dạng reference (ví dụ: secret_id).

## 3. Schema (gợi ý)

Mỗi bản ghi (`memory entry`) có thể có cấu trúc JSON như sau:

```json
{
  "entry_id": "uuid-v4",
  "request_id": "req-1234",
  "session_id": "sess-5678",
  "user_id": "user-abc",
  "agent_id": "misa",
  "timestamp": "2026-01-02T12:34:56Z",
  "short_answer": "Tóm tắt ngắn (1-2 câu)",
  "reasoning": "Chi tiết các bước tư duy hoặc bullet list",
  "confidence": 0.82,
  "tags": ["philosophy","questioning"],
  "conflict_flags": [],
  "loop_flag": false,
  "provenance": {
    "model": "gpt-x",
    "model_version": "v1",
    "prompt": "..."
  },
  "user_feedback": null
}
```

Giải thích các trường chính:
- `entry_id`: định danh duy nhất cho entry.
- `request_id`: id của request ban đầu (để nhóm nhiều proposal thuộc cùng request).
- `session_id` / `user_id`: dùng cho truy vấn theo phiên/người dùng.
- `agent_id`: agent sinh proposal (mina/mila/misa/mita/...).
- `reasoning`: bản ghi chi tiết cho audit, có thể là text dài.
- `confidence`: số 0.01.0 do agent cung cấp.
- `conflict_flags` / `loop_flag`: cờ do Mina Core gắn nếu phát hiện mâu thuẫn hoặc loop.
- `provenance`: metadata về model, prompt, source.

## 4. Ví dụ luồng lưu & truy vấn (mô phỏng)

- Khi user gửi `POST /query`, Core broadcast tới agents.
- Mỗi agent trả `proposal` và Core gọi `POST /memory/store` với payload như schema trên.
- Core sau đó có thể gọi `GET /memory/query?session_id=sess-5678` để thu lịch sử reasoning.

## 5. API mẫu (gợi ý)

- `POST /memory/store`  -> body: memory entry JSON -> trả `201 Created`.
- `GET /memory/query?session_id=...&limit=50` -> trả list các entry (theo thời gian giảm dần).
- `GET /memory/entry/{entry_id}` -> trả chi tiết một entry.
- `POST /memory/feedback` -> {entry_id, user_id, rating, comment} để gắn feedback vào entry.

## 6. Ví dụ code Python (file-based minimal)

Đoạn code này minh hoạ cách lưu truy vấn đơn giản vào file JSON (chỉ để demo):

```python
import json
from pathlib import Path
from datetime import datetime

DB = Path("./memory_store.json")

def append_entry(entry: dict):
    entries = []
    if DB.exists():
        entries = json.loads(DB.read_text(encoding="utf-8"))
    entries.append(entry)
    DB.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")

def query_session(session_id: str, limit: int = 50):
    if not DB.exists():
        return []
    entries = json.loads(DB.read_text(encoding="utf-8"))
    # lọc theo session và trả limit bản ghi mới nhất
    filtered = [e for e in entries if e.get("session_id") == session_id]
    return sorted(filtered, key=lambda x: x.get("timestamp", ""), reverse=True)[:limit]

# Ví dụ tạo entry
entry = {
    "entry_id": "id-001",
    "request_id": "req-1",
    "session_id": "sess-1",
    "user_id": "user-1",
    "agent_id": "mila",
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "short_answer": "Lập kế hoạch học 3 tháng: ...",
    "reasoning": "1) Đánh giá trình độ; 2) Chia modul; 3) Lịch học tuần",
    "confidence": 0.9,
    "tags": ["plan","action"]
}

append_entry(entry)
print(query_session("sess-1"))
```

Lưu ý: File-based chỉ dùng cho demo; production nên dùng DB (Postgres/SQLite/Mongo) với indexing cho `session_id`/`timestamp`.

## 7. Quyền riêng tư & retention

- Không lưu trực tiếp secrets (api keys, tokens). Nếu bắt buộc, lưu reference và dùng secret manager.
- Hỗ trợ xóa/anonymize theo yêu cầu user (Right to be forgotten).
- Đặt retention policy (ví dụ: 90 ngày cho logs, 3 năm cho reasoning hữu dụng), tùy chính sách.

## 8. Best practices

- Mỗi entry kèm `provenance` để biết nguồn và có thể tái tạo kết quả.
- Khi lưu nhiều proposal/entry liên quan một `request_id`, gộp lại theo nhóm để dễ audit.
- Ghi `loop_flag`/`conflict_flags` để dễ chạy báo cáo chất lượng tư duy.

## 9. Next steps (gợi ý implement)

- Tạo adapter DB (SQLite cho dev, Postgres cho staging/prod).
- Viết API nhỏ (`POST /memory/store`, `GET /memory/query`).
- Viết script migration để chuyển dữ liệu file-based sang DB khi cần.

---


