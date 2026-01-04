---

# Kế hoạch phù hợp cho bạn (8–11 giờ/tuần) + Ưu tiên CLI trước

## A) Nhịp học 8–11 giờ/tuần (gợi ý lịch cụ thể)
Bạn có thể theo 1 trong 2 nhịp dưới (đều ổn):

### Nhịp 8 giờ/tuần (4 buổi × 2 giờ)
- **Buổi 1**: học khái niệm mới + làm 1 micro‑deliverable
- **Buổi 2**: code tiếp + chạy lại demo command cho đúng output
- **Buổi 3**: sửa lỗi + viết log/notes (ghi lại bạn hiểu gì)
- **Buổi 4**: refactor nhẹ + viết 1 test nhỏ (pytest)

### Nhịp 10–11 giờ/tuần (5 buổi × 2 giờ + 1 giờ review)
- **5 buổi**: mỗi buổi tập trung 1 micro‑deliverable
- **1 giờ review/tuần**:
  - đọc lại log cũ
  - ghi “tuần này mình làm được gì”
  - liệt kê lỗi hay gặp + cách giải (tự tạo “sổ tay debug”)

> Lưu ý quan trọng: với người mới, **đều đặn** quan trọng hơn “học dồn”.  
> Chỉ cần mỗi buổi bạn chạy ra đúng “Terminal outputs mong đợi” là bạn đang đi đúng.

---

## B) CLI-first nghĩa là gì? (và vì sao nên làm)
- **CLI-first (ưu tiên dòng lệnh trước)**: sản phẩm chạy được chỉ bằng terminal, không cần UI web.
- Lợi ích:
  - Dễ debug (nhìn log/print rõ)
  - Ít phụ thuộc thư viện UI
  - MVP ra nhanh hơn
- Khi CLI chạy ổn rồi, bạn thêm UI Streamlit sau cũng rất dễ (UI chỉ là “cửa sổ” gọi lại core logic).

---

# Phase 0 – Daily plan 14 ngày (mỗi ngày ~30–60 phút, cộng dồn theo tuần)

> Mục tiêu 14 ngày: bạn tự tin Python đủ để làm orchestrator + log + file IO + test cơ bản.

## Ngày 1: Cài Python + kiểm tra version
**Bạn phải làm được**
- `python --version`
- chạy `python -c "print('OK')"`

## Ngày 2: Tạo venv (môi trường ảo)
**Thuật ngữ**
- venv (môi trường ảo): nơi cài thư viện riêng cho project
**Bạn phải làm được**
- tạo `.venv` + activate

## Ngày 3: pip + requirements.txt
**Bạn phải làm được**
- `pip install pytest`
- tạo `requirements.txt` có `pytest`

## Ngày 4: Git cơ bản (commit)
**Bạn phải làm được**
- `git init` (nếu chưa)
- commit đầu tiên: “init project”

## Ngày 5: Python function + list/dict
**Bạn phải làm được**
- viết 1 hàm nhận list số và trả tổng
- hiểu dict: `{ "task": "..." }`

## Ngày 6: Đọc/ghi file text
**Bạn phải làm được**
- ghi file `out/hello.txt`
- đọc lại và in ra

## Ngày 7: JSON cơ bản
**Bạn phải làm được**
- dump dict ra JSON file
- load JSON file lên dict

## Ngày 8: JSONL (mỗi dòng 1 JSON)
**Thuật ngữ**
- JSONL: file log, mỗi dòng là 1 record JSON
**Bạn phải làm được**
- append 3 dòng JSONL vào `data/runs/demo.jsonl`

## Ngày 9: Class cực cơ bản (OOP)
**Bạn phải làm được**
- class `Task` có `title` và `description`
- tạo object và print thuộc tính

## Ngày 10: dataclass (class dữ liệu gọn)
**Bạn phải làm được**
- chuyển `Task` sang `@dataclass`

## Ngày 11: Exception (try/except)
**Bạn phải làm được**
- bắt `FileNotFoundError` khi đọc file không tồn tại

## Ngày 12: Logging (INFO/ERROR)
**Bạn phải làm được**
- log INFO khi start, log ERROR khi có lỗi

## Ngày 13: pytest test đơn giản
**Bạn phải làm được**
- test hàm cộng số
- `pytest` chạy pass

## Ngày 14: “Mini project” tổng hợp
**Bạn phải làm được**
- chạy `python -m ...` tạo 1 file log JSONL có 3 events

---

# MVP‑0 (CLI) – Checklist 10 bước siêu tối thiểu (mỗi bước 1 file + 1 lệnh chạy)

> Mục tiêu: sau 10 bước bạn có MVP‑0 chạy end-to-end (Planner + Solver mock + loop detector + human prompt + memory JSONL).

## Bước 1: Tạo entrypoint CLI
**Tạo file**
- `src/agent_app/__main__.py`
**Lệnh chạy**
```bash
python -m agent_app
```
**Output mong đợi**
- in `AGENT APP READY`

## Bước 2: Tạo schema dữ liệu
**Tạo file**
- `src/agent_app/schema.py` (Task, Event, RunResult)
**Lệnh chạy**
```bash
python -c "from agent_app.schema import Task; print(Task)"
```

## Bước 3: Logger JSONL
**Tạo file**
- `src/agent_app/jsonl_logger.py`
**Lệnh chạy**
```bash
python -c "from agent_app.jsonl_logger import append_event; append_event('demo', {'type':'ping'})"
```
**Kết quả**
- tạo `data/runs/demo.jsonl`

## Bước 4: Agent base (giao diện agent)
**Tạo file**
- `src/agent_app/agents/base.py`
**Thuật ngữ**
- interface (giao diện): quy ước agent phải có hàm `run()`
**Lệnh chạy**
```bash
python -c "from agent_app.agents.base import Agent"
```

## Bước 5: PlannerAgent (mock)
**Tạo file**
- `src/agent_app/agents/planner.py`
**Lệnh chạy**
```bash
python -c "from agent_app.agents.planner import PlannerAgent; print(PlannerAgent().run('task'))"
```
**Kết quả**
- trả về list steps (dù đơn giản)

## Bước 6: SolverAgent (mock)
**Tạo file**
- `src/agent_app/agents/solver.py`
**Lệnh chạy**
```bash
python -c "from agent_app.agents.solver import SolverAgent; print(SolverAgent().run('step 1'))"
```

## Bước 7: Loop detector (heuristic)
**Tạo file**
- `src/agent_app/loop_detector.py`
**Thuật ngữ**
- heuristic (luật kinh nghiệm): rule đơn giản, không cần hoàn hảo
**Lệnh chạy**
```bash
python -c "from agent_app.loop_detector import is_loop; print(is_loop(['a','a','a']))"
```
**Kết quả**
- `True`

## Bước 8: Human arbitration CLI
**Tạo file**
- `src/agent_app/arbitration_cli.py`
**Lệnh chạy**
```bash
python -c "from agent_app.arbitration_cli import ask_user_choice; print(ask_user_choice('loop'))"
```
**Kết quả**
- hiện prompt chọn Continue/Modify/Stop

## Bước 9: Long-term memory JSONL
**Tạo file**
- `src/agent_app/memory_jsonl.py`
**Lệnh chạy**
```bash
python -c "from agent_app.memory_jsonl import save_memory, query_memory; save_memory({'task':'x','final':'y'}); print(query_memory('x'))"
```

## Bước 10: Orchestrator end-to-end
**Tạo file**
- `src/agent_app/orchestrator.py`
**Lệnh chạy**
```bash
python -m agent_app run --task "Tạo kế hoạch học Python 7 ngày"
```
**Output mong đợi**
- in plan, steps, final
- tạo run log JSONL
- lưu memory JSONL

---

## Gợi ý câu hỏi để bạn tự “dò mạng” học đúng
- “Python venv là gì”
- “JSONL format”
- “pytest basics”
- “Python dataclass”
- “Python logging best practices”
- “CLI argparse tutorial”