# mina-core
Multi-agent reasoning system with loop awareness, human-in-the-loop arbitration, and long-term reasoning memory.
# MINA – Essence & Core

> **Mina is not an assistant.  
> Mina is a system that reasons, disagrees, loops, and knows when to stop.**

---

## 1. Mina là gì?

**Mina** là một hệ thống AI đa tác tử (multi-agent) được thiết kế để:
- Tư duy phản biện nội bộ
- Chấp nhận chuẩn tương đối theo ngữ cảnh
- Phát hiện và kiểm soát vòng lặp logic
- Có sự tham gia của con người (*human-in-the-loop*) như một trọng tài

Mục tiêu của Mina **không phải trả lời nhanh**, mà là:
> **tạo ra reasoning có thể theo dõi, phản biện, chấm điểm và dừng đúng lúc**

---

## 2. Vấn đề Mina giải quyết

Các LLM hiện tại thường gặp các vấn đề:
- Tự tin sai (hallucination)
- Lặp tư duy nhưng không tự nhận ra
- Không có bộ nhớ reasoning dài hạn
- Không biết khi nào nên dừng hoặc nhờ con người can thiệp

👉 Mina được xây dựng để **chấp nhận những điểm yếu này là bản chất**,  
và thiết kế hệ thống **xoay quanh việc kiểm soát chúng**, thay vì che giấu.

---

## 3. Triết lý cốt lõi (Essence)

Mina vận hành dựa trên các trụ cột sau:

### 3.1 Multi-Agent Reasoning
- Nhiều agent với vai trò khác nhau
- Các agent **phản biện lẫn nhau**, không đồng thuận mù quáng

### 3.2 Relative Truth (Chuẩn tương đối)
- Không tồn tại “đúng tuyệt đối”
- Mỗi kết luận phải gắn với **ngữ cảnh + giả định**

### 3.3 Loop Awareness & Control
- Phát hiện vòng lặp suy luận
- Có cơ chế:
  - giảm độ ưu tiên
  - thay đổi chiến lược
  - hoặc dừng hẳn

### 3.4 Human-in-the-Loop
- Khi hệ thống bế tắc hoặc mâu thuẫn kéo dài
- Con người đóng vai trò **trọng tài**, không phải người suy nghĩ thay

### 3.5 Memory + Feedback
- Lưu:
  - reasoning
  - mâu thuẫn
  - phản hồi
  - điểm chất lượng tư duy
- Bộ nhớ này ảnh hưởng trực tiếp tới các vòng suy luận sau

### 3.6 Creativity as an Escape Mechanism
- Sáng tạo không phải để “hay”
- Mà để **thoát khỏi bẫy logic khép kín**

---

## 4. Kiến trúc tổng thể

Mina được tách rõ giữa **Essence (tư duy)** và **Core (hệ thống)**.

### 4.1 Mina Core
- Điều phối agent
- Quản lý vòng lặp & ưu tiên
- Quyết định khi nào cần human-in-the-loop

### 4.2 LLM API
- Chỉ đóng vai trò **bộ suy luận**
- Không giữ trạng thái dài hạn

### 4.3 Database (SQL)
- Nguồn sự thật nhất quán (source of truth)
- Lưu:
  - memory
  - feedback
  - reasoning score
  - lịch sử mâu thuẫn

### 4.4 Google Apps Script (GAS)
- Tự động hóa
- Kết nối Google Drive / Docs
- Lưu persona, log, version tư duy

### 4.5 Frontend (Dashboard)
- Hiển thị luồng suy luận
- Cho phép con người:
  - can thiệp
  - ưu tiên
  - dừng hệ thống

---

## 5. Trạng thái dự án

- 🚧 Giai đoạn: **Research / Prototype**
- 🔒 Repository: **Private**
- ⚠️ Code còn thay đổi mạnh, chưa ổn định

Dự án hiện **không nhằm mục tiêu production**,  
mà tập trung vào:
- kiến trúc
- triết lý
- khả năng mở rộng tư duy

---

## 6. Bảo mật

- Không hard-code secret
- Tất cả credential dùng `.env`
- OAuth scope giới hạn tối thiểu
- Repo public (nếu có) sẽ **không chứa dữ liệu thật**

---

## 7. Định hướng tương lai

- Chuẩn hóa loop detection
- Chấm điểm reasoning tự động
- So sánh chất lượng suy luận giữa các agent
- Tách các module để open-source có chọn lọc

---

## 8. Disclaimer

Mina **không tuyên bố là “AI đúng”**.  
Mina chỉ cố gắng trở thành:
> **một hệ thống biết mình có thể sai,  
và biết cách xử lý điều đó.**
