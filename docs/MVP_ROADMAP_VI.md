# Lộ trình học tập & MVP (Việt ngữ) cho **hệ thống suy luận đa tác tử (multi-agent)** bằng Python

> Tài liệu này **thay thế hoàn toàn** mọi nội dung liên quan Mina blockchain/node trước đây.  
> Mục tiêu: mô tả **lộ trình học tập** và **yêu cầu MVP** cho repo được định vị như một **hệ thống suy luận đa tác tử** có **nhận biết vòng lặp (loop awareness)**, **phân xử có người trong vòng lặp (human-in-the-loop arbitration)** và **bộ nhớ suy luận dài hạn (long-term reasoning memory)**.

---

## 1) Tầm nhìn sản phẩm (Product Vision)
Xây dựng một framework/ứng dụng Python cho phép nhiều tác tử (agent = “tác nhân phần mềm” có thể lập kế hoạch và hành động) phối hợp để giải bài toán, trong đó:

- **Loop awareness (nhận biết vòng lặp)**: hệ thống phát hiện khi agent đang lặp lại cùng một chu kỳ hành động/suy nghĩ (ví dụ: hỏi–đáp vòng tròn, gọi tool thất bại lặp lại) và tự áp dụng chiến lược thoát vòng lặp.
- **Human-in-the-loop arbitration (phân xử có người tham gia)**: khi các agent bất đồng hoặc độ tin cậy thấp, hệ thống tạm dừng và xin quyết định/ưu tiên từ người dùng (arbitration = “phân xử/ra quyết định cuối”).
- **Long-term reasoning memory (bộ nhớ suy luận dài hạn)**: lưu trữ bền vững các sự kiện, quyết định, ngữ cảnh dự án… để tái sử dụng qua nhiều phiên (session), tránh “mất trí nhớ” khi chạy lại.

Kết quả mong muốn: một MVP chạy được end-to-end, có giám sát vòng lặp, có cơ chế xin phán quyết của người, và có bộ nhớ dài hạn đủ dùng.

---

## 2) Người dùng mục tiêu & use-cases
### 2.1 Persona
- **Dev/Researcher** muốn thử nghiệm kiến trúc multi-agent có kiểm soát vòng lặp.
- **PM/Operator** muốn ủy quyền tác vụ (điều tra lỗi, viết tài liệu, tạo PR) nhưng cần can thiệp khi hệ thống không chắc.

### 2.2 Use-cases MVP (tối thiểu)
1. **Tìm hiểu codebase & trả lời câu hỏi**: agent đọc repo, tóm tắt module, trả lời “file này làm gì?”.
2. **Tạo kế hoạch thay đổi nhỏ**: agent đề xuất các bước sửa lỗi/viết test.
3. **Thực thi công cụ (tool use)**: chạy lệnh giả lập hoặc gọi API nội bộ (trong MVP có thể mock).
4. **Tranh luận giữa agent**: ít nhất 2 agent đưa ra phương án khác nhau và có cơ chế chọn.
5. **Xin phân xử từ người dùng**: khi bế tắc/không chắc, hệ thống hỏi người dùng chọn A/B.
6. **Nhớ quyết định**: lựa chọn của người dùng được ghi vào bộ nhớ và áp dụng về sau.

---

## 3) Kiến trúc tổng quan (High-level Architecture)
### 3.1 Thành phần chính
- **Orchestrator (bộ điều phối)**: quản lý vòng đời phiên làm việc, phân công nhiệm vụ, gom kết quả.
- **Agent**: mỗi agent có vai trò (role) riêng, ví dụ:
  - **Planner agent** (lập kế hoạch)
  - **Critic agent** (phê bình/đánh giá)
  - **Executor agent** (thực thi tool)
- **Tooling layer (lớp công cụ)**: các “tool” mà agent có thể gọi (VD: đọc file, tìm kiếm, chạy test). MVP có thể dùng tool giả lập (mock) trước.
- **Memory subsystem (hệ bộ nhớ)**:
  - **Short-term memory** (ngắn hạn): trạng thái hội thoại/phiên hiện tại.
  - **Long-term memory** (dài hạn): lưu bền (SQLite/JSONL) + chỉ mục truy hồi.
- **Loop monitor (giám sát vòng lặp)**: đo lặp (repetition), phát hiện “stuckness” (kẹt), kích hoạt chiến lược.
- **Arbitration UI/CLI**: kênh hỏi người dùng xác nhận (CLI prompt, web UI đơn giản).

### 3.2 Luồng dữ liệu (dataflow) tối thiểu
1. Người dùng nhập task.
2. Orchestrator tạo “episode” (một phiên xử lý) + nạp bộ nhớ dài hạn liên quan.
3. Planner tạo plan → Critic phản biện → Orchestrator quyết.
4. Executor thực thi tool / tạo output.
5. Loop monitor theo dõi: nếu lặp → thay chiến lược hoặc hỏi người.
6. Kết thúc: ghi tóm tắt và quyết định vào long-term memory.

---

## 4) Loop awareness: định nghĩa & yêu cầu
### 4.1 Định nghĩa
**Loop awareness** là khả năng:
- phát hiện một chuỗi trạng thái/hành động lặp lại hoặc không tiến triển;
- đo “tiến triển” bằng tiêu chí định lượng;
- có hành động can thiệp.

### 4.2 Tín hiệu phát hiện vòng lặp (MVP)
- **Repetition score (điểm lặp)**: so sánh n-gram của “thought/plan/tool call” giữa các bước; nếu giống > ngưỡng.
- **Tool failure streak (chuỗi lỗi tool)**: cùng 1 tool/cùng lỗi lặp k lần.
- **No-new-information**: 3 bước liên tiếp không tạo artifact mới (file/plan/test).

### 4.3 Chiến lược thoát vòng lặp (MVP)
- **Backoff**: tăng thời gian chờ hoặc giảm số agent.
- **Change strategy**: chuyển từ “search” sang “ask user”, hoặc từ “execute” sang “plan”.
- **Ask human**: kích hoạt phân xử (arbitration).

---

## 5) Human-in-the-loop arbitration: định nghĩa & yêu cầu
### 5.1 Định nghĩa
**Human-in-the-loop** nghĩa là con người tham gia vào vòng ra quyết định ở các điểm then chốt.  
**Arbitration** là cơ chế chọn phương án cuối cùng khi có tranh chấp/không chắc chắn.

### 5.2 Khi nào cần hỏi người dùng (MVP)
- Critic đánh giá plan rủi ro cao (risk) hoặc thiếu thông tin.
- Loop monitor báo kẹt.
- Các agent đưa ra kết luận trái ngược (conflict) và không thể tự giải.

### 5.3 Giao diện hỏi (MVP)
- CLI hỏi lựa chọn:
  - Chọn phương án A/B/C
  - Cho phép nhập “tiêu chí ưu tiên” (VD: nhanh/đúng/an toàn)
  - Cho phép “dừng” hoặc “chạy tiếp”

### 5.4 Lưu vết quyết định (audit trail)
- Log đầy đủ: ai đề xuất, lý do, ai phê bình, người dùng chọn gì.
- Lưu trong long-term memory để tái sử dụng.

---

## 6) Long-term reasoning memory: định nghĩa & yêu cầu
### 6.1 Định nghĩa
**Long-term reasoning memory** là bộ nhớ lưu trữ bền vững các “facts” (sự kiện), “decisions” (quyết định), “summaries” (tóm tắt), và có khả năng **retrieval (truy hồi)** khi cần.

### 6.2 Dạng dữ liệu tối thiểu
- **Memory item** gồm:
  - `id`, `timestamp`
  - `type`: fact/decision/summary
  - `content`: nội dung tiếng Việt/Anh
  - `tags`: nhãn để tìm
  - `source`: user/agent/tool

### 6.3 Lưu trữ (MVP)
- Ưu tiên đơn giản: **SQLite** hoặc **JSONL** (mỗi dòng 1 JSON).
- Có **index** đơn giản theo tag + tìm kiếm full-text.

### 6.4 Truy hồi (MVP)
- Top-k theo:
  - keyword match
  - tag match
  - recency (độ mới)

---

## 7) Yêu cầu MVP (Must-have)
### 7.1 Chức năng
1. **Chạy được một phiên multi-agent** với ít nhất 2 agent (Planner + Critic) + Orchestrator.
2. **Loop monitor** phát hiện lặp theo ít nhất 2 tiêu chí và kích hoạt xử lý.
3. **Arbitration**: CLI prompt để người dùng chọn phương án khi:
   - loop detected, hoặc
   - conflict giữa agent.
4. **Long-term memory**: lưu decision + summary sau mỗi phiên, và có retrieval đầu phiên.
5. **Observability (quan sát hệ thống)**:
   - log theo bước (step)
   - có “event timeline” (dòng thời gian sự kiện)

### 7.2 Phi chức năng (Non-functional)
- **Determinism tùy chọn**: cho phép seed (tái lập) ở chế độ test.
- **An toàn**: tool execution sandbox/mock trong MVP.
- **Khả năng mở rộng**: dễ thêm agent/tool.

### 7.3 Tiêu chí nghiệm thu (Acceptance Criteria)
- Demo kịch bản:
  1) User giao “tóm tắt module X và đề xuất cải tiến”.
  2) Planner đề xuất 2 phương án.
  3) Critic phản biện và chỉ ra rủi ro.
  4) Orchestrator phát hiện bất đồng → hỏi người.
  5) Người chọn 1 phương án.
  6) Hệ thống ghi quyết định vào memory.
  7) Lần chạy sau, hệ thống truy hồi và nhắc lại quyết định.

---

## 8) Lộ trình học tập (Learning Roadmap) theo tuần
> Mục tiêu: vừa học vừa hiện thực MVP. Có thể co giãn theo thời gian.

### Tuần 1 — Nền tảng Python cho agentic systems
- Củng cố:
  - typing, dataclasses/pydantic (schema dữ liệu)
  - asyncio (bất đồng bộ = chạy song song giả lập bằng event loop)
  - logging chuẩn
- Bài tập:
  - viết log events theo step
  - thiết kế schema: Task, AgentOutput, ToolCall

### Tuần 2 — Thiết kế Orchestrator & Agent interface
- Học/thiết kế:
  - interface `Agent.run(input) -> output`
  - message passing (truyền thông điệp)
  - prompt/plan structure (cấu trúc kế hoạch)
- Bài tập:
  - cài Orchestrator chạy Planner → Critic → quyết định.

### Tuần 3 — Tooling layer & sandbox
- Học:
  - pattern “tool registry” (đăng ký tool)
  - validation input/output
  - mock tool (giả lập) để test
- Bài tập:
  - tool đọc file (read-only)
  - tool search đơn giản

### Tuần 4 — Loop awareness
- Học:
  - heuristic phát hiện lặp
  - state machine (máy trạng thái) cho vòng đời episode
- Bài tập:
  - triển khai repetition score
  - triển khai tool failure streak
  - can thiệp: change strategy/ask human

### Tuần 5 — Human-in-the-loop arbitration
- Học:
  - UX cho CLI confirmation
  - conflict resolution (giải quyết xung đột)
- Bài tập:
  - hiển thị A/B, nhận lựa chọn
  - ghi audit trail

### Tuần 6 — Long-term memory
- Học:
  - SQLite/JSONL
  - full-text search cơ bản
  - tóm tắt (summary) sau phiên
- Bài tập:
  - lưu decision + summary
  - retrieval top-k đầu phiên

### Tuần 7 — Testing & evaluation
- Học:
  - pytest
  - golden tests (test theo “kết quả chuẩn”)
  - simulation runs (chạy mô phỏng)
- Bài tập:
  - test loop detection
  - test arbitration path
  - test memory retrieval

### Tuần 8 — Đóng gói & tài liệu
- Học:
  - packaging (pyproject)
  - CLI entrypoint
  - docs
- Bài tập:
  - `python -m ...` chạy demo
  - viết README hướng dẫn

---

## 9) Đề xuất cấu trúc thư mục (tham khảo)
```
repo/
  src/
    core/
      orchestrator.py
      agents/
        base.py
        planner.py
        critic.py
        executor.py
      tools/
        registry.py
        read_file.py
        search.py
      loop/
        monitor.py
        heuristics.py
      memory/
        store.py
        schema.py
        retrieval.py
      ui/
        cli.py
  tests/
    test_loop_monitor.py
    test_arbitration.py
    test_memory.py
  docs/
    MVP_ROADMAP_VI.md
```

---

## 10) Glossary (giải thích thuật ngữ nhanh)
- **Agent (tác tử)**: chương trình con có vai trò cụ thể, có thể đề xuất và hành động.
- **Orchestrator (bộ điều phối)**: thành phần điều phối nhiều agent.
- **Loop awareness (nhận biết vòng lặp)**: phát hiện kẹt/lặp và can thiệp.
- **Human-in-the-loop (người trong vòng lặp)**: có điểm dừng để người ra quyết định.
- **Arbitration (phân xử)**: chọn phương án cuối khi bất đồng.
- **Long-term memory (bộ nhớ dài hạn)**: lưu bền vững qua nhiều lần chạy.
- **Retrieval (truy hồi)**: tìm lại ghi nhớ liên quan.
- **Heuristic (phép kinh nghiệm)**: quy tắc gần đúng để phát hiện/ra quyết định.

---

## 11) TODO (ngắn) để bắt đầu ngay
1. Tạo skeleton Orchestrator + 2 agent.
2. Thêm event log theo step.
3. Viết loop monitor (repetition + tool-failure).
4. Thêm CLI arbitration.
5. Thêm memory JSONL/SQLite.
6. Viết 3 bài test chính.
