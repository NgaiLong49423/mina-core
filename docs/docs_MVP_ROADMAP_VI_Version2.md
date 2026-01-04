# Lộ trình học + MVP (siêu chi tiết) cho dự án **Multi‑Agent Reasoning System** (Python)
*(có loop awareness + human‑in‑the‑loop + long‑term memory)*

> Bạn mới học Python và đây là dự án đầu tiên: tài liệu này viết theo kiểu **đọc đi đọc lại là làm được**.  
> Mỗi thuật ngữ chuyên ngành sẽ có giải thích tiếng Việt ngay bên cạnh.

---

## 0) Định nghĩa mục tiêu (đọc 3 phút để khỏi lạc)
### Bạn muốn làm gì?
Bạn muốn làm một hệ thống trong đó nhiều “agent” phối hợp giải một “task”, có:
- **Loop awareness** (nhận biết vòng lặp): biết mình đang lặp/đang kẹt.
- **Human‑in‑the‑loop** (người trong vòng lặp): kẹt thì hỏi người quyết định.
- **Long‑term memory** (bộ nhớ dài hạn): nhớ quyết định và kinh nghiệm để lần sau dùng lại.

### MVP ở đây nghĩa là gì?
**MVP (Minimum Viable Product)** = “phiên bản tối thiểu chạy được” để chứng minh ý tưởng.  
MVP *không cần* đẹp, không cần tối ưu, không cần AI xịn. Quan trọng nhất: **end‑to‑end chạy được**.

---

## 1) Từ điển thuật ngữ (Glossary mini – đọc lướt trước)
- **Agent (tác tử/tác nhân)**: 1 module chương trình có vai trò riêng (ví dụ: Planner lập kế hoạch).
- **Orchestrator (bộ điều phối/nhạc trưởng)**: gọi các agent theo thứ tự, gom kết quả.
- **Step (bước)**: 1 lượt xử lý trong phiên chạy.
- **Trace/Log (dấu vết/nhật ký)**: ghi lại từng bước hệ thống làm gì để debug.
- **Loop (vòng lặp)**: lặp lại cùng hành vi/ý tưởng nhiều lần mà không tiến triển.
- **Heuristic (luật kinh nghiệm)**: quy tắc đơn giản để phát hiện/ra quyết định (không hoàn hảo nhưng dễ làm).
- **Human override (người sửa/ghi đè)**: người dùng sửa câu trả lời hoặc chọn phương án khác.
- **Arbitration (phân xử/chọn phương án cuối)**: cơ chế cho người chọn A/B/C khi agent bất đồng.
- **Memory (bộ nhớ)**:
  - **Short‑term** (ngắn hạn): nhớ trong 1 lần chạy.
  - **Long‑term** (dài hạn): lưu xuống file/DB để lần sau vẫn còn.
- **JSON (định dạng dữ liệu)**: dạng `{ "key": "value" }`.
- **JSONL**: mỗi dòng là 1 JSON (dễ log nhiều record).
- **CLI (dòng lệnh)**: chạy và tương tác qua terminal.
- **UI (giao diện)**: ví dụ web (Streamlit).
- **Test case (ca kiểm thử)**: input mẫu + output mong muốn.
- **Unit test (kiểm thử đơn vị)**: test từng hàm nhỏ.
- **Integration test (kiểm thử tích hợp)**: test cả chuỗi nhiều module.

---

## 2) Chia MVP thành 3 mức (để bạn không bị ngợp)

### MVP‑0 (CỰC TỐI THIỂU – làm 1 mình dễ nhất)
Mục tiêu: chạy được end‑to‑end với agent giả lập (mock agent = agent giả, chưa cần AI).

**MVP‑0 phải có**
1. Orchestrator chạy 2 agent:
   - `PlannerAgent` (lập kế hoạch)
   - `SolverAgent` (thực hiện)
2. Loop detector đơn giản:
   - Nếu cùng một output lặp ≥ 3 lần → báo loop.
3. Human‑in‑the‑loop qua CLI:
   - Khi loop, hỏi người: “tiếp tục / dừng / sửa output”.
4. Long‑term memory dạng file `data/memory.jsonl`:
   - Lưu: task + final answer + quyết định của người.
5. Trace/log lưu `data/runs/<run_id>.jsonl`.

**MVP‑0 không cần**
- Không cần LLM (AI thật)
- Không cần vector database
- Không cần web UI

---

### MVP‑1 (THÊM TOOL ĐƠN GIẢN + UI NHẸ)
Mục tiêu: agent có thể dùng tool đọc file/tìm kiếm trong repo và có UI Streamlit để xem trace.

**MVP‑1 thêm**
- Tool `read_file` (đọc file)
- Tool `search_text` (tìm chữ trong code)
- UI Streamlit:
  - nhập task
  - xem trace timeline
  - nút Accept/Modify/Reject khi loop/conflict

---

### MVP‑2 (TRÍ NHỚ TỐT HƠN + ĐÁNH GIÁ)
Mục tiêu: memory truy hồi tốt hơn và có test/evaluation rõ ràng.

**MVP‑2 thêm**
- Memory lưu SQLite (database nhẹ trong 1 file) *hoặc* JSONL + index
- Retrieval (truy hồi) top‑k theo tag/keyword + độ mới (recency)
- Bộ test cases 10–20 bài + pytest tự chạy

---

## 3) Kiến trúc tối giản (bạn cần hiểu đúng cái gì đang chạy)
### 3.1 Luồng chạy chuẩn (end‑to‑end)
1) User nhập `task`  
2) Orchestrator gọi Planner → tạo `plan` (kế hoạch gồm các bước)  
3) Orchestrator gọi Solver làm từng bước → tạo `step_results`  
4) Loop detector theo dõi, nếu lặp/kẹt → hỏi người (arbitration)  
5) Kết thúc → ghi log + ghi memory

### 3.2 “State” tối thiểu bạn cần lưu
- `run_id`: mã phiên chạy
- `task`
- `steps`: danh sách bước
- `events`: log theo bước
- `final_answer`
- `human_decisions`: người chọn gì

---

## 4) Lộ trình học (siêu căn bản) trước khi làm dự án
> Vì bạn mới học Python, mình thêm **Giai đoạn 0** thật kỹ.

## Giai đoạn 0 — Python căn bản để làm dự án (2–4 tuần)
### Mục tiêu
Bạn phải làm được 5 việc sau:
1) Tạo project, chạy Python, cài thư viện  
2) Viết hàm, dùng dict/list thành thạo  
3) Viết class đơn giản  
4) Đọc/ghi file JSON/JSONL  
5) Debug bằng print/log + hiểu error message

### Các khái niệm Python bạn phải nắm (kèm giải thích)
- **virtualenv/venv (môi trường ảo)**: nơi cài thư viện riêng cho project, không đụng hệ thống.
- **pip**: công cụ cài thư viện.
- **requirements.txt**: file danh sách thư viện.
- **module/package**: cách tổ chức code theo thư mục.
- **typing (gợi ý kiểu dữ liệu)**: giúp code dễ đọc (không bắt buộc nhưng rất tốt).
- **dataclass**: cách tạo class dữ liệu ngắn gọn.

### Bài tập “phải làm”
- Bài 1: ghi 10 dòng JSONL vào file và đọc lại.
- Bài 2: tạo class `Task` và `RunResult`.
- Bài 3: viết function `detect_repeat(outputs: list[str]) -> bool`.

**Output bạn phải nhìn thấy**
- Chạy `python main.py` in ra “OK”
- Tạo được file `.jsonl` có nội dung đúng

---

## 5) Roadmap theo tuần (kèm micro‑deliverables: làm xong sẽ thấy gì)
> Bạn có thể đi theo nhịp **8–12 tuần** tuỳ giờ/tuần.  
> Nếu ít thời gian: mỗi “tuần” hiểu là 1 “chặng”.

### Tuần 1 — Setup project + chạy “hello orchestrator”
**Mục tiêu**
- Repo có cấu trúc, chạy được một lệnh demo.

**Việc làm**
- Tạo `src/` và `data/`
- Tạo `src/main.py`
- Tạo `requirements.txt` (tạm thời có thể trống)

**Bạn phải nhìn thấy**
```bash
$ python -m src.main
RUN OK
```

---

### Tuần 2 — Schema dữ liệu (Task/Step/Event) + logging JSONL
**Thuật ngữ**
- **Schema (lược đồ dữ liệu)**: bạn định nghĩa dữ liệu vào/ra có những trường gì.

**Việc làm**
- Tạo `Task`, `Event`, `RunState` (dataclass)
- Hàm `append_event(run_id, event)` ghi vào `data/runs/<run_id>.jsonl`

**Bạn phải nhìn thấy**
- File log được tạo, mỗi dòng là 1 JSON hợp lệ.

---

### Tuần 3 — Agents mock (Planner + Solver) chạy được
**Việc làm**
- `PlannerAgent`: biến task thành 3 bước cố định (ví dụ: “Hiểu yêu cầu → Lên kế hoạch → Trả lời”)
- `SolverAgent`: xử lý từng bước (chỉ cần trả text)

**Bạn phải nhìn thấy**
- Terminal in ra plan + final answer
- Log có các event: planner_output, solver_step_1, solver_step_2…

---

### Tuần 4 — Loop detector (phát hiện vòng lặp) bản đơn giản
**Thuật ngữ**
- **Loop detector (bộ phát hiện vòng lặp)**: nhìn vào chuỗi output và quyết định “có đang lặp không”.

**Việc làm**
- Rule 1: nếu output giống nhau ≥ 3 lần → loop
- Rule 2: nếu step index không tăng (bị kẹt) → loop

**Bạn phải nhìn thấy**
- Khi cố tình tạo output lặp, hệ thống báo:
```text
LOOP DETECTED. Need human decision.
```

---

### Tuần 5 — Human‑in‑the‑loop qua CLI (arbitration)
**Việc làm**
- Khi loop/conflict, hỏi user:
  - 1) Continue (tiếp tục)
  - 2) Modify answer (sửa)
  - 3) Stop (dừng)

**Bạn phải nhìn thấy**
- Bạn nhập lựa chọn trong terminal và hệ thống áp dụng đúng.

---

### Tuần 6 — Long‑term memory dạng JSONL
**Việc làm**
- File `data/memory.jsonl` lưu:
  - task
  - final_answer
  - human_decision
  - timestamp
- Đầu phiên chạy mới: tìm lại memory theo keyword đơn giản (ví dụ: chứa từ khoá giống task)

**Bạn phải nhìn thấy**
- Lần chạy sau, hệ thống in:
```text
Found 1 relevant memory item(s). Applying suggestion...
```

---

### Tuần 7 — (Tuỳ chọn) Streamlit UI để xem trace
**Thuật ngữ**
- **Streamlit**: thư viện Python làm web UI nhanh.

**Việc làm**
- `ui/streamlit_app.py`:
  - input task
  - nút Run
  - hiển thị events timeline
  - chỗ nhập override khi loop

**Bạn phải nhìn thấy**
- Mở web local và xem trace theo bước.

---

### Tuần 8 — Test (pytest) + README
**Việc làm**
- Unit test:
  - loop detector
  - memory save/load
- README:
  - cách cài
  - cách chạy demo
  - 1 kịch bản demo

**Bạn phải nhìn thấy**
```bash
$ pytest
3 passed
```

---

## 6) Lịch học gợi ý theo giờ/tuần (để bạn tự lượng sức)
### Nếu bạn có ~6 giờ/tuần
- 3 buổi × 2 giờ
- Mỗi buổi:
  1) đọc 20’ (hiểu 1 khái niệm)
  2) code 80’
  3) ghi chú 20’ (log lại mình làm được gì)

### Nếu ~10 giờ/tuần
- 5 buổi × 2 giờ
- 2 buổi chỉ để sửa bug + đọc log

### Nếu ~15 giờ/tuần
- 5 buổi × 3 giờ
- Thêm 1 buổi “refactor + viết test”

---

## 7) Cấu trúc thư mục đề xuất (dễ cho người mới)
```
src/
  main.py
  core/
    orchestrator.py
    schema.py
    logger_jsonl.py
    loop_detector.py
    memory.py
    agents/
      base.py
      planner.py
      solver.py
ui/
  streamlit_app.py   (tuỳ chọn)
data/
  runs/
  memory.jsonl
tests/
  test_loop_detector.py
  test_memory.py
README.md
requirements.txt
```

---

## 8) Checklist hoàn thành (đánh dấu xong là “có MVP”)
### MVP‑0 checklist
- [ ] Chạy được `python -m src.main`
- [ ] Planner + Solver mock hoạt động
- [ ] Log JSONL theo step
- [ ] Loop detector phát hiện lặp
- [ ] CLI hỏi người khi loop
- [ ] Memory JSONL lưu quyết định
- [ ] Có 5 demo tasks

### MVP‑1 checklist
- [ ] Tool read_file + search_text
- [ ] UI Streamlit xem trace + override

### MVP‑2 checklist
- [ ] pytest tests chạy pass
- [ ] 10–20 test cases
- [ ] memory retrieval tốt hơn (top‑k)

---

## 9) Ghi chú quan trọng để bạn không bỏ cuộc
- Dự án đầu tiên: **đừng làm quá khó ngay**. MVP‑0 xong đã là thắng lớn.
- Khi bí: nhìn log JSONL. Debug = đọc log.
- Mỗi tuần chỉ cần “thấy được output” là tiến bộ.

---

## 10) Nếu bạn muốn mình kèm sát (đề xuất cách hỏi)
Bạn có thể gửi:
- ảnh lỗi terminal
- file `data/runs/<run_id>.jsonl`
- đoạn code orchestrator/loop_detector

Mình sẽ chỉ đúng chỗ sai và gợi ý cách sửa theo mức bạn đang học.