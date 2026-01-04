# mina-core
Multi-agent reasoning system with loop awareness, human-in-the-loop arbitration, and long-term reasoning memory.
# MINA – Essence & Core

> **Mina is not just an assistant.  
> Mina is a system that reasons, disagrees, loops, and knows when to stop.  
> Mina presents itself as the User Dashboard.**

---

## 1. Mina là gì?

**Mina** là một hệ thống AI đa tác tử (multi-agent) được thiết kế để:
- Tư duy phản biện nội bộ và có khả năng phản biện lại cả User, dựa trên dữ liệu thực tế để đưa ra phản biện có căn cứ
- Chấp nhận chuẩn tương đối theo ngữ cảnh, không giả định tồn tại chuẩn tuyệt đối
- Phát hiện và kiểm soát vòng lặp logic
- Có sự tham gia của con người (*human-in-the-loop*) như một trọng tài, và cũng có thể là một "nhân vật" trong quá trình tư duy phản biện cùng AI – nhưng luôn có **quyền ưu tiên cao nhất**, vì hệ thống xoay quanh User chứ không phải AI
- Là hệ thống học tập từ dữ liệu quá khứ của cả chính nó và của User

Mục tiêu của Mina **không phải trả lời nhanh**, mà là:
> **tạo ra reasoning có thể theo dõi, phản biện, chấm điểm và dừng đúng lúc;  
> cho User thấy cái nhìn tổng quan nhất, còn quyết định cuối cùng là ở User;  
> Hệ thống không quyết định hộ, mà đưa ra đánh giá và bức tranh toàn cảnh, đồng thời có khả năng tự vận hành với chính nó dưới sự giám sát hoặc can thiệp của User.**

---

## 2. Vấn đề Mina giải quyết

Các LLM hiện tại thường gặp các vấn đề:
- Tự tin sai (hallucination)
- Lặp tư duy nhưng không tự nhận ra
- Không có bộ nhớ reasoning dài hạn
- Không biết khi nào nên dừng hoặc nhờ con người can thiệp
- Không chạy ngầm, không biết khi nào đang "hoạt động", phải nhờ con người tự nhắc
- Đưa ra thông tin một chiều, thiếu chiều sâu và thiếu bối cảnh lịch sử của User
- Thiếu dữ liệu thật, tự dùng logic chính nó để suy diễn rồi dẫn đến sai
- Không chấp nhận mình sai dù đã có User nhắc nhở

👉 Mina được xây dựng để **chấp nhận những điểm yếu này là bản chất**,  
và thiết kế hệ thống **xoay quanh việc kiểm soát chúng**, thay vì che giấu.

---

## 3. Triết lý cốt lõi (Essence)

Mina vận hành dựa trên các trụ cột sau:

### 3.1 Multi-Agent Reasoning
- Nhiều agent với vai trò khác nhau, trong đó có một agent đặc biệt là **User**
- Các agent **phản biện lẫn nhau**, không đồng thuận mù quáng
- User là người đưa ra quyết định cuối cùng, hoặc có thể **ủy quyền** cho một agent khác theo mức độ ưu tiên được thiết kế ban đầu
- Mục tiêu cao nhất của mỗi agent là đặt mình vào vị trí User và lựa chọn phương án có lợi nhất cho User.


### 3.2 Relative Truth (Chuẩn tương đối)
- Không tồn tại “đúng tuyệt đối”
- Mỗi kết luận phải gắn với **ngữ cảnh + giả định + dữ liệu thật**
- Hệ thống và cả User cần hiểu lựa chọn đó đánh đổi gì: **lợi ích, rủi ro, và cái giá phải trả**

### 3.3 Loop Awareness & Control

**Khi không có User can thiệp trực tiếp (No User mode):**

- Phát hiện vòng lặp suy luận
- Có cơ chế:
  - giảm độ ưu tiên của chiến lược/agent đang lặp
  - thay đổi chiến lược suy luận
  - hoặc dừng hẳn vòng suy luận

**Khi có User tham gia đối thoại (Yes User mode):**

- Vẫn phát hiện vòng lặp, nhưng:
  - Các agent khởi đầu với mức ưu tiên tương đương
  - Ưu tiên được tăng/giảm qua từng vòng đối thoại với User dựa trên chất lượng reasoning
  - Có thể thay đổi chiến lược, gợi ý hướng suy nghĩ mới cho User
  - Có thể tự động chốt hoặc để User tự chốt khi đã đủ thông tin

### 3.4 Human-in-the-Loop

**No User (tự vận hành):**

- Khi hệ thống bế tắc hoặc mâu thuẫn kéo dài
- Con người đóng vai trò **trọng tài**, không phải người suy nghĩ thay

**Yes User (User đang tương tác):**

- Khi hệ thống và User cùng thấy bế tắc hoặc mâu thuẫn kéo dài
- Con người và hệ thống cùng đóng vai trò **trọng tài**, cùng đề xuất lựa chọn tối ưu
- Nếu User không đồng tình, hệ thống tiếp tục chạy, phản biện và cập nhật đề xuất
### 3.5 Memory + Feedback

- Lưu:
  - reasoning
  - mâu thuẫn
  - phản hồi
  - điểm chất lượng tư duy
  - dữ liệu và lịch sử tương tác của người dùng
  - dữ liệu thực tế xoay quanh người dùng, làm bằng chứng phản biện vững chắc nhất
  - tư duy và các phản biện của người dùng → cơ sở để tạo ra các **agent ảo** mô phỏng phong cách suy nghĩ của User (khi được User cho phép)

- Bộ nhớ này ảnh hưởng trực tiếp tới các vòng suy luận sau:  
  hệ thống không chỉ “nhớ thông tin”, mà còn **nhớ cách User suy nghĩ**.

### 3.6 Creativity as an Escape Mechanism

- Sáng tạo không phải để “nghe hay”
- Mà để **thoát khỏi bẫy logic khép kín** của AI và cả User,  
  tìm các góc nhìn mới khi mọi hướng suy luận quen thuộc đều bế tắc

## 3.7 Quyền kiến trúc & quyền quyết định cuối

Mina là một hệ thống được **thiết kế có chủ đích**,  
không phải hệ thống biểu quyết theo số đông.

Hệ thống cho phép:
- nhiều agent cùng tranh luận và phản biện,
- phản biện lại cả User,
- lặp suy luận để đào sâu vấn đề.

Tuy nhiên:

- Không agent nào (kể cả AI hay User-agent) có quyền quyết định cuối cùng.
- Quyết định không được suy ra bằng việc “đa số đồng ý”.

**Quyền dừng, quyền chấp nhận hoặc bác bỏ cuối cùng thuộc về người giữ vai trò kiến trúc sư hệ thống Mina.**

Người giữ vai trò này chịu trách nhiệm về:
- tầm nhìn tổng thể của Mina,
- các ranh giới không được phép vượt qua,
- thời điểm nào là “đủ để dừng suy nghĩ”,
- và hệ quả dài hạn của hệ thống.

Mina có thể tiếp tục tranh luận, gợi ý hoặc tự vận hành,
**chỉ khi quyền này chưa được người kiến trúc sư sử dụng.**

---

## 4. Kiến trúc tổng thể

Mina được tách rõ giữa **Essence (tư duy)** và **Core (hệ thống)**.

### 4.1 Mina Core
- Điều phối agent
- Quản lý vòng lặp & ưu tiên
- Quyết định khi nào cần human-in-the-loop
- Quản lý dữ liệu được nạp vào trong vòng phản biện, từ chối hoặc cho phép các agent lấy dữ liệu trên database nếu vẫn tuân thủ các nguyên tắc đã được thiết kế

### 4.2 LLM API
- Chỉ đóng vai trò **bộ suy luận**
- Không giữ trạng thái dài hạn
- Có thể yêu cầu thêm dữ liệu từ Mina Core hoặc trực tiếp yêu cầu User cung cấp thêm bối cảnh thực tế
- Có khả năng từ chối trả lời khi đang ở trong vòng lặp, hoặc khi không thể tính toán luồng suy luận một cách hợp tác với các agent khác 

### 4.3 Database (SQL)
- Nguồn sự thật nhất quán (source of truth)
- Lưu:
  - memory
  - feedback
  - reasoning score
  - lịch sử mâu thuẫn
  - dữ liệu người dùng (ưu tiên hàng đầu), cùng lịch sử tương tác của người dùng

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
biết cách xử lý điều đó,  
và đủ dũng cảm để chứng minh khi User sai.**

---
