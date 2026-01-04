# MINA — Prototype specification (Phase 1)

Mục tiêu Phase 1: có một prototype chạy được mô phỏng multi-agent reasoning, lưu reasoning vào bộ nhớ đơn giản, và thể hiện hai chế độ hành vi **No-User / Yes-User** để demo ý tưởng.

> Ghi chú: tài liệu có phần ví dụ flow kéo dài tới Phase 2/3 để minh hoạ cách tranh luận (không mở rộng scope Phase 1).

## Executive summary

MINA là prototype multi-agent phục vụ để minh họa quy trình tranh luận/đề xuất giữa nhiều agent với `User` trong vòng lặp reasoning đơn giản; Phase 1 tập trung vào bản chạy nhẹ (CLI/API), lưu trữ reasoning và cơ chế human-in-the-loop.

## Table of contents

- [Scope (Phase 1)](#scope-phase-1)
- [Out of scope (Phase 1)](#out-of-scope-phase-1)
- [Agents (Phase 1)](#agents-phase-1)
- [Phase 2](#phase-2-trường-hợp-user-đồng-ý-với-1-phương-án)
- [One reasoning flow (example)](#one-reasoning-flow-example)
- [Một số chức năng ngoài lề](#một-số-chức-năng-ngoài-lề)

## Scope (Phase 1)

- Backend nhẹ (Python) chạy dưới dạng CLI / simple API (không cần dashboard “xịn”).
- 4 agents mô phỏng: `Mina (Logic)`, `Mila (Thực dụng)`, `Misa (Triết lý)`, `Mita (Thấu cảm)` + `User` (agent đặc biệt).
- Simple memory: file JSON hoặc SQLite để lưu câu hỏi, các bước reasoning, điểm đơn giản, và lịch sử tương tác.
- Loop detection heuristics cơ bản (vòng lặp số lần, hoặc trả lời lặp lại).
- Human-in-the-loop: cơ chế gọi `User` khi mâu thuẫn hoặc khi cần chốt quyết định.

## Out of scope (Phase 1)

- Google Apps Script (GAS) tích hợp Drive/Docs.
- Frontend dashboard phức tạp (chỉ demo bằng CLI hoặc trang HTML rất đơn giản).
- Nâng cao chấm điểm reasoning tự động (machine-learned scorers).

## Agents (Phase 1)

### Mina Core (backend)

`Mina Core` đưa ra **tất cả dữ liệu liên quan** đến vấn đề mà `User` đưa ra, nhằm cho một bức tranh toàn cảnh tối đa có thể. Core **không đưa đáp án**, chỉ đưa dữ liệu. Core có thể chấp thuận yêu cầu “đòi thêm dữ liệu” từ các agent khác nếu không vi phạm nguyên tắc.

### Vai trò từng agent

| Agent  |      Vai trò          | Hành vi điển hình |
|--------|-----------------------|---|
| `Mina` | Thực tế / logic       | Đề xuất phương án dựa trên dữ liệu ban đầu; cảm xúc bằng không. |
| `Mila` | Thực dụng / hành động | Đánh giá phương án, ưu tiên lợi ích và hành động; nếu đồng tình thì củng cố, nếu không thì phản biện và đề xuất phương án thay thế. |
| `Misa` | Triết lý / hậu quả    | Phân tích sâu về hậu quả, khác biệt giữa lý thuyết và thực tế; củng cố hoặc phản bác dựa trên phân tích. |
| `Mita` | Thấu cảm / cảm xúc    | Đánh giá góc nhìn cảm xúc của người dùng; cân nhắc cái giá phải trả và hậu quả cảm xúc. |

**Điều kiện dừng**

- Dừng khi chỉ còn đúng **1 phương án/đáp án**: tất cả đều đồng tình (hoặc cùng biến tấu từ một giải pháp gốc).
- Hiển thị “frontend” qua màn hình: liệt kê các phương án/đáp án cho `User` xem để đồng ý hoặc phản bác.

### `User` (agent đặc biệt)

`User` có thể tham gia trực tiếp ở giai đoạn này:

- (1) Đồng ý → kết thúc phase.
- (2) Không đồng ý với mọi giải pháp → cung cấp thêm dữ liệu.
- (3) Phản bác và đưa thêm 1 phương án.

## Phase 2 (trường hợp: `User` đồng ý với 1 phương án)

`Mina Core` cho tranh luận tiếp tục, nhưng có thêm một số chức năng mới:

- Agents có thể **từ chối trả lời**, chờ câu trả lời của agents khác, hoặc đồng suy nghĩ.
- Các agents phải trả lời được: vì sao người dùng không đồng ý, vì sao vẫn chưa vừa ý, và vì sao người dùng đang bắt đầu nghiêng về agent kia.

Ví dụ mô tả vai trò:

- `Mina`: có thể dùng dữ liệu mới từ Phase 1; có nhiều biến số do người dùng bổ sung nên có cơ hội đưa ra phương án khác. Có thể từ chối trả lời để chờ lượt hoặc yêu cầu agent khác trả lời trước.
- `Mila`: khi trả lời, lựa chọn của agent ở lượt đầu tiên có thể thêm dữ liệu hoặc không. Nếu sắp xếp theo “quyền lực” thì càng về sau càng yếu dần → `Mita` là agent cuối, gần như không còn “đặc quyền”.

Mọi thứ lặp lại cho đến khi người dùng chọn được phương án đúng ý nhất, hoặc có 1 phương án mà cả 4 agent đồng thuận và bổ trợ cho nhau.

## One reasoning flow (example)

**User:** “Nay tao buồn.”

### Phase 1

**Mina Core (backend):** đưa ra dữ liệu đang có: bài tập chưa làm xong; trời đang rất nắng; mới sốt xong mấy ngày trước; tiền sắp hết.

- `Mina`: có khả năng người dùng buồn là do trời nắng hoặc mệt → khuyên đi ngủ trưa để tối có sức làm bài tập.
- `Mila`: “hỏi quyền Mina Core” xem bài tập có nhiều không → `Mina Core` trả lời “có”. Kết luận người dùng buồn vì bài tập chất đống → khuyên làm bài, xong là hết buồn.
- `Misa`: nghĩ sâu xa; có thể buồn do “lên cơn”/tâm lý; khen vài câu cho hết buồn; đề xuất ngủ trưa như `Mina`, tối làm bài. Phản biện việc “giờ này làm” theo `Mila` là không hợp lý.
- `Mita`: thấu cảm; khuyên cố gắng làm xong bài tập để bớt buồn.

**Mina Core tổng hợp:** các agent gợi ý bớt buồn bằng cách ngủ trưa (`Mina`, `Misa`) hoặc làm bài tập (`Mila`, `Mita`).

**User phản hồi:** không đồng tình quyết định nào bên trên: “Buồn là do phân vân nên đi bơi với đám bạn không nhưng mà bài tập còn nhiều quá.”

### Phase 2

**Mina Core (backend):** bổ sung dữ liệu: bài tập rất nhiều, đang chất đống (để các agent đánh giá tiếp).

- `Mina`: từ chối trả lời để đợi xem `Mita` đưa phương án vì chuyện này liên quan đến cảm xúc/bạn bè → `Mina Core` đồng ý cho phép `Mina` trả lời sau `Mita`.
- `Mila`: không đồng ý vì sau khi xem xét bài tập thì `User` không đủ khả năng hoàn thành trước deadline. Việc đi bơi với bạn bè là không cần thiết → nhất quyết từ chối.
- `Misa`: “tôi nghĩ” nên huỷ kèo; với thời gian hiện tại, nếu không cố gắng thì rất khó xử lý bài tập.
- `Mita`: hãy lắng nghe trái tim; bạn đang đợi; cứ thoải mái đi chơi cho đời vui. Bài tập thì cố gắng hết sức sẽ xong.
- `Mina`: cũng nghiêng về việc bỏ kèo để đi học; nếu rớt môn thì “toang” (vì thấy đã rớt 2 môn).

**Mina Core tổng hợp:** nhiều agent khuyên bỏ kèo để đi học vì việc học đang quan trọng.

**User phản hồi:** không đồng ý vì buổi đi chơi này là crush rủ; muốn đi chơi để cân bằng việc học.

### Phase 3

**Mina Core (backend):** bổ sung dữ liệu về người mà `User` crush mấy năm; đây là trường hợp hiếm có cần xem xét kỹ.

- `Mila`: đã trả lời đầu ở lượt trước nên giờ trả lời tiếp; yêu cầu quyền trả lời cuối vì đang thiếu dữ liệu → Core đồng ý chuyển xuống cuối.
- `Misa`: cũng yêu cầu quyền trả lời cuối vì thiếu dữ liệu → Core từ chối vì lượt này `Mila` là người trả lời đầu tiên nên quyền mạnh nhất; cho `Misa` trả lời trước `Mila`.
- `Mita`: lần đi chơi này phải đáng nhớ; cố gắng tạo ấn tượng tốt với crush. Gợi ý mang thêm sách vở vì lên đó có thể có người chỉ bài nên học nhanh hơn.
- `Mina`: không đồng tình với `Mita`: không ai đi bơi mà mang sách vở; mang sách có thể ảnh hưởng người khác. Khuyên hẹn khi khác đi chơi; giờ vẫn đầu tư vào học.
- `Misa`: đề xuất đơn giản hơn: rủ crush về nhà dạy học cho `User`; nếu tốt thì vẫn còn thời gian đi bơi.
- `Mila`: phương án tối ưu: `User` đi bơi với crush nhưng rút ngắn (khoảng 3 tiếng) rồi xin về sớm “có việc”; thời gian còn lại vẫn đủ nếu thức đêm ôn bài. Thực tế trong database, `User` đã làm tương tự và thành công.

**Kết quả:** `User` đồng ý với cách của `Mila` → kết thúc.

## Một số chức năng ngoài lề

- Cơ chế “mức độ yêu thích” của `User` đối với từng agent. Nếu `User` càng thường xuyên đồng ý với ý kiến của một agent thì điểm ưu tiên của agent đó càng cao; điểm này có thể được dùng để sắp xếp vị trí tranh luận của agent ở Phase 1 (phản biện trước hoặc sau). Đây là loại dữ liệu nhạy cảm mà các agent không bao giờ được truy cập trực tiếp.
- Agent đặc biệt `User Proxy`: chọn phương án mà nó cho là gần với lựa chọn thường thấy của `User` nhất; không tham gia tranh luận, chỉ quan sát và bỏ phiếu. Nếu sau Phase 2 mà `User Proxy` vẫn không “hài lòng” với bất kỳ phương án nào, hệ thống sẽ mời `User` thật vào để đưa ra quyết định cuối cùng.
- Khả năng chạy ngầm để đưa ra cảnh báo theo thời gian thực kèm theo bằng chứng cụ thể, ví dụ:
	- `Mita` có thể cảnh báo khi nhận thấy tín hiệu người dùng đang bất ổn về mặt cảm xúc, đồng thời chủ động gửi lời an ủi và gợi ý cách cân bằng lại.
	- `Mila` có thể cảnh báo khi dữ liệu thực tế cho thấy bài tập hoặc công việc đang bị tồn đọng và gia tăng, từ đó nhắc nhở hoặc cảnh cáo người dùng với nhiều mức độ khác nhau.
- Định kỳ (ví dụ cuối tuần), `Mina Core` có thể tổng hợp một báo cáo ngắn về trạng thái của người dùng trong tuần: mức độ tiến bộ, các khu vực đang sa sút, xu hướng đáng chú ý và những khuyến nghị hành động quan trọng.

