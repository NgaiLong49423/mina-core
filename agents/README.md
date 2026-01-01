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
### Mina Core (blackend): đưa ra tất dữ liệu liên quan đến vấn đề mà User đưa ra. Cho một bức tranh toàn cảnh hết mức có thể, không đưa đáp án chỉ đưa dữ liệu. Có thể chấp thuận Agents khác khi đòi thêm dữ liệu nếu không quy phạm nguyên tắc.
- `Mina`: Là một người thực tế / logic nó sẽ đưa ra một phương án với dữ liệu ban đầu nó có một cách logic và thực tế nhất cảm xúc bằng không.
- `Mila`: Và giờ đây nó đã có thêm dữ liệu mà Mina đưa ra phương án và đánh giá phương án của Mina. Luôn ưu tiên lợi ích/hành động trước không quan tâm gì. đồng tình thì thêm dữ liệu cũng cố cho Mina, không đồng tình thêm dữ liệu phản bác và ra một phương án/đáp án.
- `Misa`: Tiếp Đánh giá phương án của `Mila`, `Mina`. Cái giá cũng luôn luôn ưu tiên lợi ít là gì và lý thuyết khác với thực tế như thế nào suy nghĩ thì sâu xa. Hậu quả sẽ ra sao. Đồng tình thì cũng cố tiếp luận điểm hoặc phương án của agent đó, không đồng tình thêm dữ liệu phản bác và ra một phương án/đáp án.
- `Mita`: Chính là một biến số Cảm xúc không thể nào biết trước được. Đánh giá phương án của `Mila`, `Mina`, `Misa`. Suy nghỉ cho người dùng có đáng phải đánh đổi không. Hậu quả sẽ ra sao. Đồng tình củng cố cho agent đó bằng dữ liệu mà nó đưa ra, không đồng tình thêm dữ liệu phản bác và ra một phương án/đáp án.
==> Dừng lại khi còn đúng 1 phương án/đáp án với tất cả đều đồng tình hoặc biến tấu tí của cùng một giải pháp gốc. 
==> Hiện ra frontend qua màn hình. tất cả các phương án/đáp án cho User xem đồng ý hoặc phản bác
- `User` (agent đặc biệt): có thể tham gia trực tiếp ở giai đoạn này; 1 đồng ý kết thúc phase; 2 đồng tình không đồng ý với mọi giải cho thêm dữ liệu, 3 phản bác thêm 1 phương án.

### Phase 2 (Trường hợp 1:  `User` đồng ý với với 1 phương án nào đó)
### Mina Core sẽ cho tranh luận tiếp tục Nhưng có thêm một sô chức năng mới, bây giờ các Agents có khả năng từ chối trả lời, đợi câu trả lời của các Agent Khác, đồng suy nghĩ với các Agents khác. Và các Agents khác phải trả lời đc tại sao người dùng không đồng ý, tại sao vẫn chưa vừa ý người dùng, tại sao người dùng lại người dùng đang bắt đầu nghiên về agents kia.
- `Mina`: Sang bên đây có thể dự liễu mới từ Phase 1, có cả một dữ liệu đầy biến số như người dùng  thêm một cơ hội đưa ra phương án. Nó có thể từ chối trả lời để chờ tới lượt nào đó hoặc đòi Agent trả lời trước.
-`Mila` : là agents mà trả lời thì các chọn của Agent đầu tiền nó sẽ có thêm dữ liệu hoặc không. Nhưng nếu sắp xếp theo quyền lực thì càng xuống càng yếu dần => Mita là Agents là cuối gần như không đặc quyền xịn nữa.
=> Mọi thứ sẽ lặp lại cho đến khi người dùng chọn đc phương án đúng ý nhất. Hoặc 1 phương án mà cả 4 đứa đồng thuận và bổ trợ cho nhau

One reasoning flow (example)
User: Nay tao buồn.
## Phase 1:
### Mina Core (blackend): đưa ra dữ liệu đang có bài tập chưa làm xong. Trời đang nắng thấy bà cố. Mới sốt xong mấy ngày trước. Tiền đang sắp hết.
`Mina` : Có khả năng người dùng buồn là do trời nắng hoặc mệt khuyên đi ngủ trưa để tối có sức làm bài tập
`Mila` : "Hỏi quyền Mina Core" :xem bài tập có nhiều không => Mina có trả lời là "có". À thằng người dùng buồn vì đang có bài tập chất đống khuyên làm bài đi mày. Xong là hết buồn
`Misa` : Nghĩ sâu xa. Có lẽ thằng này buồn là do lên cơn thôi. Khen nó mấy câu cho hết buồn. Nay chắc trời nắng quá thôi anh ngủ đi tối làm bài tập như Mina nói. Là sáng mai tự hết buồn à. Mila khuyên giờ này làm là không đúng đâu anh đừng nghe không hợp lý.
`Mita` : Thấu cảm thấy buồn cùng anh vì thế giới này khổ với anh quá. Thôi cố găng đi làm xong bài tập là hết buồn à.
### Mina Core đánh giá tổng quan. Agents khuyên anh nên làm gì đó bớt buồn đi có thể đi ngủ như Mina và Misa làm bài tập như Mila và Mita
==> User: Không đồng tình với quyết định nào bên trên. "Buồn là do phân vân nên đi bơi với đám bạn không nhưng mà bài tập còn nhiều quá"

## Phase 2:
### Mina Core (blackend): Cho thêm dữ liệu về bài tập rằng rất nhiều bài tập đang chất đống. Gồm nhưng gì những gì cho các Agents đánh giá tiếp
`Mina` : Thì chối trả lời vì muốn đợi xem Mita đưa gia phương án vì chuyện này liên quan để cảm xúc bạn bè ==> Mina Core đồng ý cho phép Mina trả lời sau Mita.
`Mila` : Không được vì sau khi xem xét bài tập thì thấy User không đủ khả năng hoàn thành bài tập trong thời hạn deadline.
Việc đi bơi với bạn bè là không cần thiết. Nhất quyết từ chối
`Misa` : Tôi nghỉ anh nên hủy kèo đi tôi thấy Mila nói đúng đấy việc với thời gian hiện tại việc anh hoàn toàn khó làm sao bài tập mà không cố gắng
`Mita` : Hãy lắng nghe trái tim anh đi. Bạn đang đợi anh nên anh cứ thoải mái đi chơi cho đời thêm vui. Bài tập thì cố gắng hết sức là làm xong à
`Mina` : Tôi cũng nên thấy anh bỏ kèo đi học đi không rớt môn thì toan tối thấy anh đã rớt 2 môn rồi đấy.
### Mina Core đánh giá tổng quan. Nhiều Agents khuyên anh nên bỏ kèo để đi học vì học đang rất là quan trọng đối với anh.
==> User: Tôi không đồng ý vì buồi đi chơi này là Crush rủ tôi. Nên tôi muốn đi chơi cân bằng việc học lun.

## Phase 3:
### Mina Core: Cho thêm dữ liệu về người mà User crush mấy năm này rồi đây là một trường hợp hiếm có cần phải xem xét kĩ.
`Mila`: Là người trả lời đầu lúc nãy nên giờ trả lời tiếp. Yêu cầu quyền trả lời cuối cùng vì đang thiếu dữ liệu. Core đồng ý chuyển xuống cuối
`Misa`: Cũng yêu cầu quyền trả lời cuối vì thiếu dữ liệu. Core từ chối vì lượt này Mila là người trả lời đầu tiền nên quyền mạnh nhất. Cho Misa trả lời trước Mila.
`Mita`: Hãy anh phải khiến lần đi chơi này đáng nhớ mới được cố gắng tạo ấn tượng tốt với crush. Hãy mang thêm sách vở nữa vì lên đó thì sẽ có người chỉ bài nên học nhanh hơn.
`Mina`: Không đồng tình với Mita. Không bạn nào đi bơi ngoài user đi bơi mà mang theo sách vở đâu. Việc user mang thêm sách vở còn ảnh hưởng đến người khác. Tôi khuyên thay vì tự chối nên hẹn khi khác đi chơi. Giờ vẫn đầu tư vào học
`Misa`: Hay bây giờ đơn giản hơn. Kêu crush về nhà dạy học cho user sẽ tốt hơn nhanh hơn nếu tốt sẽ vẫn còn thời gian đi bơi.
`Mila`: Cách tối nhất bây giờ user nên đi bơi với Crush đi nhưng đi chơi ít lại thôi khoảng 3 tiếng là xin về sớm có việc. Khoảng thời gian còn lại vẫn đủ nếu user thức đêm ôn bài. Vì thực tế cho thấy trong database user cũng đã làm đc điểu tương tự với cách này và thành công
==> User đồng ý với cách Mila. 
==> Kết thúc

## Một số chức năng ngoài lề
- Có mức độ yêu thích của user về Agents. Nếu User đồng ý với ý kiến của Agents càng nhiều thì điểm ưu thích cảng cao. Nó có thể đẩy Agents phản biện đầu tiên hoặc cuối cùng ở Phase 1. Đây là dữ liệu quan trọng mà các Agents không bao giờ đc biết
- Agents (đặc biệt): là User Proxy nó sẽ chọn mà nó nghĩ User hay chọn nhất nhưng nó không có quyền tranh luận nếu nó không đồng ý quá Phase 2 thì gọi user ra chọn dùm.

