# MINA MVP-0 - Multi-Agent Reasoning System

Hệ thống suy luận đa tác tử (Multi-Agent Reasoning) với 4 agents: Mina, Mila, Misa, Mita.

## Tính năng

- ✅ 4 agents với vai trò khác nhau (Logic, Thực dụng, Triết lý, Thấu cảm)
- ✅ Loop detection - phát hiện vòng lặp reasoning
- ✅ Memory system - lưu reasoning history
- ✅ Human-in-the-loop - hỗ trợ Yes-User và No-User mode
- ✅ Tích hợp Gemini API
- ✅ Tích hợp Google Drive (tùy chọn) để load persona files

## Cài đặt

1. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

2. Set biến môi trường:
```bash
# Windows PowerShell
$env:GEMINI_API_KEY = "your-api-key-here"

# Linux/Mac
export GEMINI_API_KEY="your-api-key-here"
```

3. (Tùy chọn) Nếu muốn dùng Google Drive để load personas:
- Đặt `credentials.json` trong `Mina_Core/secrets/`
- Set `MINA_SECRETS_DIR` nếu dùng thư mục khác

## Sử dụng

### Chạy với task đơn giản:

```bash
python -m MVP-0.src.main --task "Nay tao buồn"
```

### Với các tùy chọn:

```bash
python -m MVP-0.src.main \
  --task "Nay tao buồn" \
  --max-loops 3 \
  --memory-file data/memory.jsonl \
  --use-drive \
  --user-mode
```

### Các tham số:

- `--task`: Câu hỏi/nhiệm vụ cho agents (bắt buộc)
- `--memory-file`: Đường dẫn file lưu memory (mặc định: `data/memory.jsonl`)
- `--max-loops`: Số vòng reasoning tối đa (mặc định: 5)
- `--use-drive`: Load personas từ Google Drive
- `--user-mode`: Yes-User mode (mặc định: True)
- `--api-key`: Gemini API key (hoặc dùng biến môi trường)

## Cấu trúc

```
MVP-0/
├── src/
│   ├── core/
│   │   ├── __init__.py      # Package exports
│   │   ├── agent.py          # Base Agent class
│   │   ├── agents.py         # Specific agents (Mina, Mila, Misa, Mita)
│   │   ├── orchestrator.py   # Mina Core orchestrator
│   │   ├── memory.py         # Memory storage system
│   │   └── loop_detection.py # Loop detection mechanism
│   └── main.py               # CLI entry point
├── data/
│   └── memory.jsonl          # Reasoning history (tự động tạo)
└── requirements.txt
```

## Agents

### Mina (Logic)
- Vai trò: Thực tế / logic
- Hành vi: Đề xuất phương án dựa trên dữ liệu ban đầu; cảm xúc bằng không

### Mila (Thực dụng)
- Vai trò: Thực dụng / hành động
- Hành vi: Đánh giá phương án, ưu tiên lợi ích và hành động

### Misa (Triết lý)
- Vai trò: Triết lý / hậu quả
- Hành vi: Phân tích sâu về hậu quả, khác biệt giữa lý thuyết và thực tế

### Mita (Thấu cảm)
- Vai trò: Thấu cảm / cảm xúc
- Hành vi: Đánh giá góc nhìn cảm xúc của người dùng; cân nhắc cái giá phải trả

## Ví dụ output

```
============================================================
MINA MVP-0 - Multi-Agent Reasoning System
============================================================

Loading agent personas...
✓ Loaded persona for Mina
✓ Loaded persona for Mila
✓ Loaded persona for Misa
✓ Loaded persona for Mita

Initializing MINA Core orchestrator...
✓ Orchestrator ready

User task: Nay tao buồn
------------------------------------------------------------

============================================================
REASONING RESULTS
============================================================

[1] Mina:
    Có khả năng người dùng buồn là do trời nắng hoặc mệt → khuyên đi ngủ trưa để tối có sức làm bài tập.
    Confidence: 0.80

[2] Mila:
    Bài tập có nhiều không → khuyên làm bài, xong là hết buồn.
    Confidence: 0.75

[3] Misa:
    Có thể buồn do "lên cơn"/tâm lý; đề xuất ngủ trưa như Mina, tối làm bài.
    Confidence: 0.70

[4] Mita:
    Thấu cảm; khuyên cố gắng làm xong bài tập để bớt buồn.
    Confidence: 0.65

------------------------------------------------------------
SUMMARY:
=== Tổng hợp phản hồi từ các agents ===

Mina: Có khả năng người dùng buồn là do trời nắng hoặc mệt → khuyên đi ngủ trưa để tối có sức làm bài tập....
Mila: Bài tập có nhiều không → khuyên làm bài, xong là hết buồn....
Misa: Có thể buồn do "lên cơn"/tâm lý; đề xuất ngủ trưa như Mina, tối làm bài....
Mita: Thấu cảm; khuyên cố gắng làm xong bài tập để bớt buồn....

Total loops: 1
============================================================
```

## Phát triển tiếp

- [ ] Tích hợp với database SQL thay vì JSONL
- [ ] Cải thiện loop detection với ML
- [ ] Thêm reasoning scoring tự động
- [ ] Frontend dashboard
- [ ] User Proxy agent
- [ ] Background monitoring và alerts

## License

Private project - Research/Prototype phase.

