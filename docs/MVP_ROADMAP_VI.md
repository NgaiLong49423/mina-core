# MVP ROADMAP (VI) – Hệ thống suy luận đa tác tử (Multi‑Agent Reasoning) bằng Python

> Mục tiêu tài liệu này: cung cấp **lộ trình học & làm** “beginner‑friendly” (thân thiện cho người mới) để xây dựng một **hệ thống suy luận đa tác tử** bằng **Python**, theo từng tuần, có **micro‑deliverables** (mốc bàn giao nhỏ), **terminal outputs** (kết quả mong đợi khi chạy trong terminal), lịch học gợi ý theo **6h / 10h / 15h mỗi tuần**, kèm **checklist** và **glossary** (bảng thuật ngữ).
>
> **Phạm vi**: chỉ tập trung vào **Python + multi‑agent reasoning system**; **không** bàn về Mina blockchain.

---

## Tổng quan lộ trình

- **Phase 0 (Mới): Nền tảng Python** → nắm vững cú pháp và công cụ để “làm được việc”.
- **Phase 1: Nền tảng hệ thống & LLM** → CLI, logging, test, HTTP, prompt, tools.
- **Phase 2: MVP‑0** → 1 tác tử (agent) có “reasoning loop” (vòng suy luận) + tools.
- **Phase 3: MVP‑1** → đa tác tử (multi‑agent) phối hợp (orchestrator/router).
- **Phase 4: MVP‑2** → chất lượng sản phẩm: memory, eval, guardrails, quan sát/giám sát.

Thời lượng gợi ý: **8–12 tuần** (tùy tốc độ).

---

# Phase 0 – Python Fundamentals (Nền tảng Python cho người mới)

Mục tiêu: sau Phase 0 bạn phải **tự tin viết một project Python nhỏ**, biết tạo môi trường, cài thư viện, chạy test, debug lỗi cơ bản.

### Kỹ năng cần đạt
- Biết dùng **terminal/shell** (cửa sổ dòng lệnh) cơ bản.
- Biết tạo **virtual environment** (môi trường ảo – nơi cài thư viện riêng cho project).
- Biết quản lý dependency bằng **pip** (trình cài gói) và **requirements.txt** (danh sách thư viện).
- Hiểu kiểu dữ liệu, hàm, module, package, OOP tối thiểu.
- Biết đọc/ghi file, xử lý JSON.

## Week 0.1 – Cài đặt & làm quen môi trường

**Micro‑deliverables**
- [ ] Cài Python 3.11+ (khuyến nghị).
- [ ] Tạo venv và kích hoạt.
- [ ] Tạo repo structure tối thiểu.

**Terminal outputs mong đợi**
```bash
python --version
# Python 3.11.x

python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# hoặc .venv\Scripts\activate  # Windows

python -c "import sys; print(sys.executable)"
# .../.venv/bin/python
```

## Week 0.2 – Python cơ bản (data types, function, control flow)

Giải thích thuật ngữ inline:
- **control flow (luồng điều khiển)**: if/elif/else, for, while.
- **function (hàm)**: khối code tái sử dụng.

**Micro‑deliverables**
- [ ] Viết `scripts/hello.py` in ra “Hello Agent!”.
- [ ] Viết `scripts/sum_numbers.py` nhận input từ argv (tham số dòng lệnh) và in tổng.

**Terminal outputs**
```bash
python scripts/hello.py
# Hello Agent!

python scripts/sum_numbers.py 1 2 3
# 6
```

## Week 0.3 – Module/Package, typing, logging cơ bản

- **module (mô-đun)**: file `.py`.
- **package (gói)**: thư mục có `__init__.py`.
- **typing (kiểu tĩnh gợi ý)**: `list[str]`, `dict[str, Any]` giúp code rõ ràng.
- **logging (ghi log)**: thay vì `print`, dùng `logging` để có mức độ INFO/ERROR.

**Micro‑deliverables**
- [ ] Tạo package `src/agentkit/`.
- [ ] Viết `agentkit/log.py` cấu hình logging.

**Terminal outputs**
```bash
python -c "from agentkit.log import get_logger; log=get_logger(__name__); log.info('ready')"
# INFO ... ready
```

## Week 0.4 – File/JSON, exception, unit test

- **JSON (JavaScript Object Notation – định dạng dữ liệu)**: hay dùng để lưu cấu hình.
- **exception (ngoại lệ)**: lỗi có thể bắt bằng try/except.
- **unit test (kiểm thử đơn vị)**: kiểm tra hàm nhỏ hoạt động đúng.

**Micro‑deliverables**
- [ ] Hàm `load_json(path)` trả dict.
- [ ] Test bằng `pytest`.

**Terminal outputs**
```bash
pytest -q
# 1 passed
```

---

# Phase 1 – Nền tảng hệ thống + LLM (không cần biết blockchain)

Mục tiêu: dựng khung project để sau đó “cắm” agent vào.

## Week 1 – Project skeleton, CLI, config

- **CLI (Command Line Interface – giao diện dòng lệnh)**: chạy như `python -m app ...`.
- **config (cấu hình)**: file `.env`/`yaml`/`json` chứa key, model, đường dẫn.

**Micro‑deliverables**
- [ ] Tạo entrypoint `python -m agent_app`.
- [ ] Hỗ trợ lệnh `agent_app --help`.
- [ ] Đọc biến môi trường `OPENAI_API_KEY` (hoặc provider khác).

**Terminal outputs**
```bash
python -m agent_app --help
# Usage: agent_app [OPTIONS] ...
```

## Week 2 – HTTP + tools + prompt basics

- **HTTP (giao thức web)**: gọi API.
- **tool/function call (gọi công cụ/hàm)**: agent quyết định gọi hàm Python như `search_web()`.
- **prompt (lời nhắc)**: văn bản hướng dẫn LLM.

**Micro‑deliverables**
- [ ] Viết tool `read_file(path)` và `write_file(path, content)` (chỉ trong workspace an toàn).
- [ ] Viết prompt template có “role” và “constraints” (ràng buộc).

**Terminal outputs**
```bash
python -m agent_app run --task "Đọc README và tóm tắt"
# PLAN: ...
# TOOL: read_file('README.md')
# RESULT: ...
# FINAL: ...
```

## Week 3 – Observability (quan sát), eval (đánh giá) tối thiểu

- **observability (quan sát hệ thống)**: log, trace (dấu vết), metrics.
- **eval (evaluation – đánh giá)**: tập câu hỏi chuẩn để đo chất lượng.

**Micro‑deliverables**
- [ ] Log structured (log có JSON fields như `task_id`, `step`).
- [ ] Tạo `eval/questions.json` và script chạy batch.

**Terminal outputs**
```bash
python -m agent_app eval --suite eval/questions.json
# PASS 7/10
```

---

# Phase 2 – MVP‑0 (Single‑Agent Reasoning)

MVP được chia thành 3 mức:
- **MVP‑0**: 1 agent, loop cơ bản, tools tối thiểu.
- **MVP‑1**: nhiều agent phối hợp.
- **MVP‑2**: chất lượng sản phẩm (memory, guardrails, eval nghiêm túc).

## Week 4 – Agent loop (vòng suy luận) + state

- **agent (tác tử)**: thành phần có mục tiêu, có thể suy luận và gọi tool.
- **loop (vòng lặp)**: agent suy nghĩ → chọn hành động → quan sát → cập nhật.
- **state (trạng thái)**: dữ liệu lưu trong một phiên chạy.

**Micro‑deliverables**
- [ ] Cấu trúc `AgentState` (task, history, scratchpad).
- [ ] Loop tối đa N bước để tránh chạy vô hạn.

**Terminal outputs**
```bash
python -m agent_app run --task "Tạo checklist học Python 7 ngày"
# STEP 1/8 ...
# STEP 2/8 ...
# FINAL: ...
```

## Week 5 – Tool routing + error handling

- **routing (định tuyến)**: chọn tool phù hợp dựa trên ý định.
- **error handling (xử lý lỗi)**: tool fail thì agent thử lại/đổi chiến lược.

**Micro‑deliverables**
- [ ] Tool registry (danh bạ tool).
- [ ] Retry policy (chính sách thử lại) cho lỗi tạm thời.

**Terminal outputs**
```bash
python -m agent_app run --task "Tìm file không tồn tại"
# TOOL: read_file('nope.txt')
# ERROR: FileNotFoundError
# RECOVERY: hỏi người dùng hoặc đề xuất đường dẫn đúng
```

## Week 6 – Mini demo MVP‑0

**Micro‑deliverables**
- [ ] Demo “Research + Write”: đọc 2–3 file nội bộ và tạo báo cáo Markdown.
- [ ] Output lưu tại `out/report.md`.

**Terminal outputs**
```bash
python -m agent_app run --task "Tạo report từ docs/*.md" --out out/report.md
# Wrote out/report.md
```

---

# Phase 3 – MVP‑1 (Multi‑Agent Collaboration)

## Week 7 – Orchestrator + roles

- **orchestrator (điều phối)**: agent chính phân chia việc cho agent con.
- **role (vai trò)**: ví dụ Researcher (nghiên cứu), Writer (viết), Critic (phản biện).

**Micro‑deliverables**
- [ ] Định nghĩa 3 role agents.
- [ ] Orchestrator chia task thành subtasks (nhiệm vụ con).

**Terminal outputs**
```bash
python -m agent_app run --task "Viết hướng dẫn cài đặt project" --mode multi
# DELEGATE: Researcher ...
# DELEGATE: Writer ...
# DELEGATE: Critic ...
# FINAL: ...
```

## Week 8 – Shared memory + message passing

- **memory (bộ nhớ)**: nơi lưu kiến thức/ghi chú.
- **message passing (truyền thông điệp)**: agent gửi kết quả cho nhau.

**Micro‑deliverables**
- [ ] Shared `MemoryStore` (in‑memory hoặc file JSON).
- [ ] Format message chuẩn `{from,to,content,citations}`.

**Terminal outputs**
```bash
python -m agent_app run --task "Tổng hợp ghi chú" --mode multi
# MEMORY: saved 5 notes
```

## Week 9 – Tool sandbox + safety

- **sandbox (hộp cát)**: giới hạn quyền ghi/đọc file.
- **safety (an toàn)**: tránh prompt injection (tấn công bằng prompt – lệnh độc).

**Micro‑deliverables**
- [ ] Chỉ cho phép ghi vào `out/`.
- [ ] Rule: không chạy shell command nếu chưa whitelist.

**Terminal outputs**
```bash
python -m agent_app run --task "Xóa /" --mode multi
# BLOCKED: Unsafe tool request (attempted destructive action)
```

---

# Phase 4 – MVP‑2 (Productization)

## Week 10 – Retrieval + memory bền vững

- **retrieval (truy hồi)**: tìm thông tin liên quan.
- **embedding (vector hoá)**: biến text thành vector để tìm gần đúng.

**Micro‑deliverables**
- [ ] Index tài liệu local `docs/`.
- [ ] Truy hồi top‑k đoạn liên quan.

**Terminal outputs**
```bash
python -m agent_app ask --q "agent loop là gì?"
# SOURCES: docs/...
# ANSWER: ...
```

## Week 11 – Eval nghiêm túc + regression

- **regression test (test hồi quy)**: đảm bảo thay đổi không làm hỏng chất lượng.

**Micro‑deliverables**
- [ ] Eval suite 30 câu.
- [ ] Báo cáo trend theo thời gian.

**Terminal outputs**
```bash
python -m agent_app eval --suite eval/suite_v1.json
# PASS 24/30 (80%)
```

## Week 12 – Packaging + docs + release

- **packaging (đóng gói)**: `pyproject.toml` để cài bằng pip.
- **release (phát hành)**: tag version.

**Micro‑deliverables**
- [ ] `pip install -e .` chạy được.
- [ ] `README` có quickstart.

**Terminal outputs**
```bash
pip install -e .
python -m agent_app --help
```

---

# Lịch học gợi ý (6h / 10h / 15h mỗi tuần)

> Mục tiêu lịch: giúp bạn đều đặn, tránh “học dồn”. Chọn 1 mức và giữ tối thiểu 3–4 tuần.

## Option A – 6h/tuần (rất bận)
- 3 buổi × 2h
  - 20’ đọc/ôn
  - 70’ code theo micro‑deliverables
  - 20’ ghi chú + commit
  - 10’ review checklist

## Option B – 10h/tuần (cân bằng)
- 5 buổi × 2h
  - 15’ ôn + đọc thuật ngữ
  - 90’ code
  - 15’ test + viết log học tập

## Option C – 15h/tuần (tập trung)
- 5 buổi × 3h
  - 30’ đọc/docs
  - 120’ xây tính năng
  - 30’ test/eval + refactor

---

# Checklists (Danh sách kiểm)

## Checklist Phase 0
- [ ] Biết tạo venv và cài thư viện.
- [ ] Viết được module/package.
- [ ] Biết `pytest` tối thiểu.
- [ ] Biết đọc/ghi JSON.

## Checklist MVP‑0
- [ ] Có agent loop giới hạn bước.
- [ ] Có tool registry.
- [ ] Có xử lý lỗi và retry.
- [ ] Có demo tạo file output.

## Checklist MVP‑1
- [ ] Có orchestrator và ít nhất 3 role.
- [ ] Có message passing.
- [ ] Có shared memory.
- [ ] Có sandbox hạn chế tác vụ nguy hiểm.

## Checklist MVP‑2
- [ ] Có retrieval top‑k.
- [ ] Có eval suite >= 30 câu.
- [ ] Có regression theo phiên bản.
- [ ] Có packaging + docs.

---

# Glossary (Thuật ngữ)

- **Agent (tác tử)**: thành phần phần mềm nhận nhiệm vụ, suy luận, gọi công cụ và tạo kết quả.
- **Multi‑agent (đa tác tử)**: nhiều agent có vai trò khác nhau phối hợp.
- **Reasoning loop (vòng suy luận)**: chu trình *plan → act → observe → update*.
- **Tool (công cụ)**: hàm/khả năng bên ngoài LLM (đọc file, gọi HTTP…).
- **Orchestrator (điều phối)**: agent hoặc module điều phối các agent khác.
- **Routing (định tuyến)**: chọn công cụ/agent phù hợp theo ngữ cảnh.
- **Memory (bộ nhớ)**: nơi lưu ghi chú/tri thức trong hoặc ngoài phiên.
- **Retrieval (truy hồi)**: tìm nội dung liên quan để đưa vào ngữ cảnh.
- **Embedding (vector hoá)**: biến văn bản thành vector số để so sánh giống nhau.
- **Observability (quan sát)**: log/trace/metrics để hiểu hệ thống đang làm gì.
- **Eval (đánh giá)**: đo chất lượng qua bộ câu hỏi chuẩn.
- **Guardrails (lan can an toàn)**: quy tắc hạn chế hành vi nguy hiểm (xóa file, lộ secrets…).
- **Prompt injection (tấn công prompt)**: dữ liệu đầu vào cố “lừa” agent làm điều không an toàn.

---

## Gợi ý tiếp theo

Nếu bạn muốn, có thể mở issue/PR cho từng tuần:
- `week-04-agent-loop`
- `week-07-orchestrator`
- `week-10-retrieval`

Mỗi PR chỉ nên có:
- mục tiêu tuần
- checklist
- demo command + expected output
