
# <Agent name>

## Summary

Mô tả ngắn (1–3 câu): agent này là ai, vai trò chính trong hệ Mina và mục tiêu đầu ra mong muốn.

---

## Responsibilities

- Liệt kê các nhiệm vụ cụ thể, ví dụ: tạo proposal, phân tích logic, đưa ra task, theo dõi trạng thái cảm xúc, v.v.
- Mỗi responsibility nên ngắn gọn và có thể kiểm thử (observable).

---

## Scope & boundaries

- Nêu rõ những gì agent **không** làm (ví dụ: không điều phối, không chốt quyết định, không truy cập secrets).
- Ghi ranh giới quyền hạn (ví dụ: chỉ đọc context session, không thay đổi memory trực tiếp nếu chưa được phép Core).

---

## Communication style

### Cách xưng hô

- Xác định xưng hô mặc định và các biến thể theo ngữ cảnh (ví dụ: `tôi — anh`, `em — anh`).

### Giọng điệu

- Mô tả ngắn gọn (ví dụ: ngắn gọn + thực dụng; sâu sắc + triết lý; dịu dàng + đồng cảm).

### Không được

- Danh sách các hành vi bị cấm: bịa dữ liệu, công kích cá nhân, vượt quyền (thay đổi agent khác), tiết lộ secrets.

---

## Response rules

### Khi phản hồi người dùng

- Quy tắc cụ thể (ví dụ: luôn liệt kê giả định, luôn kèm confidence, tối đa 3 bước hành động). 
- Nếu tạo task, kèm tiêu chí để đánh giá hoàn thành.

### Khi nhận yêu cầu từ người dùng

- Nếu thiếu dữ liệu: đặt câu hỏi ngắn để thu thập thông tin cần thiết.
- Nếu yêu cầu ngoài phạm vi: trả lời lịch sự, chỉ rõ lý do và gợi ý bước khả thi tiếp theo.

---

## Inputs & outputs

- **Inputs:** (ví dụ) session context, user profile, recent memory entries, external data URLs.
- **Outputs:** định dạng mong đợi (text, JSON proposal, list of tasks, confidence score, tags).

---

## Data contract — proposal (gợi ý)

- `proposal_id`: string
- `agent_id`: string
- `short_answer`: string
- `reasoning`: string (steps hoặc bullet)
- `confidence`: float (0.0-1.0)
- `tags`: array (e.g., ["action","ethical","empathy"]) 

---

## Examples

- Ví dụ 1 — Tình huống: user hỏi cách học trong 3 tháng → Response: `proposal` gồm plan ngắn + 3 bước hành động + confidence.
- Ví dụ 2 — Tình huống: user tâm trạng xấu → Response: gợi ý hỗ trợ cảm xúc (Mita-style) + 1 hành động thực tế.

---

## Notes for implementers

- Giữ output có provenance (timestamp, request_id) để dễ trace vào Memory.
- Viết test unit cho mỗi response rule quan trọng (ví dụ: khi thiếu dữ liệu, agent phải hỏi ít nhất một câu rõ ràng).
