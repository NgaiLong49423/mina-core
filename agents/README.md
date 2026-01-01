# MINA — Prototype specification (Phase 1)

Mục tiêu Phase 1: có một prototype chạy được mô phỏng multi-agent reasoning, lưu reasoning vào bộ nhớ đơn giản, và thể hiện hai chế độ hành vi No-User / Yes-User để demo ý tưởng.

Scope (Phase 1)
- Backend nhẹ (Python) chạy dưới dạng CLI / simple API (không cần dashboard xịn)
- 4 agents mô phỏng: `Mina (Logic)`, `Mila (Thực dụng)`, `Misa (Triết lý)`, `Misa (thấu cảm)` + `User` (agent đặc biệt)
- Simple memory: file JSON hoặc SQLite để lưu câu hỏi, các bước reasoning, điểm đơn giản, và lịch sử tương tác
- Loop detection heuristics cơ bản (vòng lặp số lần, hoặc trả lời lặp lại)
- Human-in-the-loop: cơ chế gọi User khi mâu thuẫn hoặc khi cần chốt quyết định

Out of scope (Phase 1)
- Google Apps Script (GAS) tích hợp Drive/Docs
- Frontend dashboard phức tạp (chỉ demo bằng CLI hoặc trang HTML rất đơn giản)
- Nâng cao chấm điểm reasoning tự động (machine-learned scorers)

### Agents (Phase 1)
### Mina Core (blackend): đưa ra tất dữ liệu liên quan đến vấn đề mà User đưa ra. Cho một bức tranh toàn cảnh hết mức có thể, không đưa đáp án chỉ đưa dữ liệu.
- `Mina`: Chính là máy móc không cảm xúc cần toàn cảnh, không cần vội sinh phương án/đáp án ban đầu dựa trên prompt. cần vội sinh ra nhiều dữ liệu tổng quát nhất cho các agents xem xét và đánh giá.
- `Mila`: đánh giá phương án của Mina nếu không có tự sinh ra phương án/đáp án trên prompt. Luôn ưu tiền lợi ích trước không quan tâm gì. Đồng tình tăng 1 bậc ưu tiên thêm dữ liệu để chứng minh phương pháp/đáp án trên là ổn, khồng đồng tình thêm dữ liệu phản bác và ra một phương án/đáp án.
- `Misa`: Đánh giá phương án của `Mila`, `Mina`. Cái giá cũng luôn luôn ưu tiên lợi ít là gì và lý thuyết khác với thực tế như thế nào. Hậu quả sẽ ra sao. Đồng tình tăng 1 bậc ưu tiên và thêm dữ liệu để chứng minh phương pháp trên là ổn, khồng đồng tình thêm dữ liệu phản bác và ra một phương án/đáp án.
- `Mita`: Chính là một biến số Cảm xúc không thể nào biết trước được. Đánh giá phương án của `Mila`, `Mina`, `Misa`. Suy nghỉ cho người dùng có đáng phải đánh đổi không. Hậu quả sẽ ra sao. Đồng tình tăng 1 bậc ưu tiên và thêm dữ liệu, khồng đồng tình thêm dữ liệu phản bác và ra một phương án/đáp án.
==> Dừng lại khi còn đúng 1 phương án/đáp án. 
==> Hiện ra frontend qua màn hình. tất cả các phương án/đáp án cho User xem đồng ý hoặc phản bác
- `User` (agent đặc biệt): có thể tham gia trực tiếp ở giai đoạn này; 1 đồng ý kết thúc phase; 2 đồng tình cộng tăng 1 bậc ưu tiên cho một phương án, 3 phản bác thêm 1 phương án.

### Phase 2 (Trường hợp 1:  `User` đồng ý với với 1 phương án nào đó)
- `Mina`: Tiếp tục không vội đưa ra phương pháp/đáp án mới. Đưa thêm dữ liệu tại sao User lại không đồng ý với các phương án đã có. Điều chỉnh hoặc cho một phương pháp/đáp án khác

One reasoning flow (example)
1. User nhập prompt/question.
2. `Generator` tạo 2 phương án A1, A2.
3. `Critic` phản biện từng phương án, cung cấp điểm và lý do.
4. `Arbiter` so sánh, nếu chênh lệch rõ ràng thì chọn; nếu mâu thuẫn hoặc score gần nhau, hỏi User chốt (Yes-User mode) hoặc áp heuristic (No-User mode).
5. Lưu toàn bộ trace vào memory với timestamp, scores, và tag (No-User / Yes-User).

No-User vs Yes-User (behavior)
- No-User: hệ thống tự vận hành; loop detection dừng sau N vòng hoặc khi agent lặp lại cùng ý; Arbiter áp heuristic (ví dụ: chọn phương án có score cao nhất trung bình).
- Yes-User: khi User tương tác, hệ thống hiển thị tóm tắt reasoning và gợi ý; User có thể chốt quyết định hoặc yêu cầu thêm vòng reasoning; ưu tiên agent có lịch sử tốt với User.

Memory schema (brief)
- `id`, `prompt`, `timestamp`
- `steps`: list of {agent, output, score, reasoning_text}
- `final_decision`, `mode` (No-User/Yes-User)
- `user_feedback` (optional)

Acceptance criteria (Phase 1)
- Can run a demo: input → agents run → saved trace → final decision output
- Loop detection triggers on repeated outputs or after configured max rounds
- User can be prompted to resolve ties and their choice stored

Milestones (suggested)
1. Week 1–2: write spec (this doc) + agent stubs
2. Week 3–4: implement `backend/main.py` with simulated agents + JSON memory
3. Week 5: test flows, record example traces, write backend README for demo

Privacy note
- Phase 1 stores user data locally only (JSON/SQLite). Any future sharing or cloud sync must include explicit consent and encryption.

---

Nếu bạn đồng ý với scope này, tôi sẽ tiếp theo tạo/điền các file: `agents/README.md`, scaffold `backend/main.py`, và `memory/README.md` theo todo đã tạo.
