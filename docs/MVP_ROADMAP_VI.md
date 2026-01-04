# Lộ trình học (Roadmap) & Yêu cầu MVP (Minimum Viable Product) – Tiếng Việt

> **Mục tiêu tài liệu này**: Cung cấp **lộ trình học Mina** theo từng giai đoạn và một **bộ yêu cầu MVP** (Minimum Viable Product – *phiên bản sản phẩm tối thiểu có thể chạy được*) để bạn có thể đóng góp/triển khai tính năng trong hệ sinh thái Mina một cách thực tế.
>
> **Đối tượng**: Người đã có nền tảng lập trình (ưu tiên OCaml/Rust/Typescript) và muốn hiểu Mina từ góc nhìn kỹ thuật (node, protocol, zk, tooling).

---

## 1) Tổng quan: Mina là gì (theo góc nhìn kỹ thuật)

- **Mina Protocol** là blockchain tập trung vào **zero-knowledge** (bằng chứng không tiết lộ – *chứng minh một điều đúng mà không lộ dữ liệu gốc*), đặc biệt là **zk-SNARKs** (*bằng chứng ngắn gọn, dễ kiểm tra, không tiết lộ*).
- Mina có kiến trúc dùng **SNARK** để giữ trạng thái chuỗi “nhẹ” hơn, và dùng **Proof-of-Stake** (bằng chứng cổ phần – *chọn người tạo block dựa trên lượng stake*) cho đồng thuận.

**Thuật ngữ nhanh**:
- **Node** (nút mạng): máy chạy phần mềm Mina, tham gia P2P.
- **P2P** (peer-to-peer – *mạng ngang hàng*): các node giao tiếp trực tiếp.
- **Ledger** (sổ cái): trạng thái tài khoản/balances.
- **Consensus** (đồng thuận): cơ chế chọn chain hợp lệ (Mina dùng Ouroboros Samasika – biến thể PoS).
- **Mempool** (bể giao dịch): nơi node giữ giao dịch chưa vào block.
- **RPC** (Remote Procedure Call – *gọi hàm từ xa*): API để wallet/ứng dụng giao tiếp với node.

---

## 2) Lộ trình học theo giai đoạn

### Giai đoạn 0 — Chuẩn bị nền tảng

**Mục tiêu**: đủ nền để đọc code, build, debug.

- Học/ôn:
  - **Linux + networking** (TCP/UDP, DNS, ports).
  - **Git** (branch, rebase, commit conventions).
  - **Docker** (container – *đóng gói môi trường chạy*): để tái lập môi trường.
  - **OCaml** (ngôn ngữ chính trong mina-core): syntax cơ bản, module system, dune.
- Kỹ năng:
  - Build dự án, chạy test, đọc log.
  - Dùng **Grafana/Prometheus** (giám sát – *quan sát metrics*) nếu repo có.

**Kết quả cần đạt**:
- Build được project từ source và chạy được ít nhất 1 binary/node mode (nếu dự án hỗ trợ).

---

### Giai đoạn 1 — Hiểu cấu trúc repo & luồng chạy node

**Mục tiêu**: biết code nằm ở đâu, data đi qua những module nào.

- Đọc:
  - README, docs nội bộ.
  - Cấu trúc thư mục `src/`, `docs/`, `scripts/`.
- Hiểu luồng:
  - Startup: parse config → init logger → init network → sync chain → start producing/validating.
  - **Config** (cấu hình): file/flags quyết định node chạy ra sao.

**Bài tập đề xuất**:
- Tìm các điểm vào chương trình (main entrypoints).
- Chạy node ở chế độ “connect/testnet” (nếu có) hoặc “sandbox/devnet” (mạng dev – *mạng thử nghiệm nội bộ*).

---

### Giai đoạn 2 — Consensus, block, ledger và mempool

**Mục tiêu**: hiểu 4 khối quan trọng của blockchain node.

1) **Block** (khối):
- Chứa header + body (giao dịch, snark work…).
- **Header** (đầu khối): metadata (parent hash, state hash…).

2) **Consensus** (đồng thuận):
- Logic chọn chain tốt nhất.
- **Finality** (tính chắc chắn): mức độ “khó bị đảo ngược” của block.

3) **Ledger** (sổ cái):
- Thường là cấu trúc Merkle (cây băm – *cho phép chứng minh phần tử thuộc tập*).
- Hỗ trợ tạo/verify **Merkle proof** (bằng chứng Merkle).

4) **Mempool**:
- Policy nhận giao dịch: fee, nonce, signature.
- Chống spam: rate limit.

**Bài tập đề xuất**:
- Trace một giao dịch: RPC submit → vào mempool → inclusion trong block → ledger update.

---

### Giai đoạn 3 — zk-SNARK: khái niệm tối thiểu để đọc code

**Mục tiêu**: không cần thành chuyên gia crypto, nhưng hiểu được “ai tạo proof, ai verify, proof gắn với cái gì”.

- **Circuit** (mạch – *mô hình ràng buộc toán học*): biểu diễn logic cần chứng minh.
- **Prover** (bên tạo proof): tạo bằng chứng.
- **Verifier** (bên kiểm tra): kiểm tra proof nhanh.
- **Trusted setup** (thiết lập tin cậy – *giai đoạn tạo tham số*): có/không tuỳ hệ.
- **Recursive proofs** (bằng chứng đệ quy – *proof chứng minh việc verify proof khác*): giúp nén lịch sử.

**Bài tập đề xuất**:
- Tìm nơi code định nghĩa circuit/constraints (nếu có).
- Xem pipeline: generate proof → verify proof → attach to block/state.

---

### Giai đoạn 4 — Networking (P2P) & Sync

**Mục tiêu**: hiểu node đồng bộ dữ liệu.

- **Gossip** (truyền tin lan truyền): cơ chế broadcast giao dịch/blocks.
- **Sync** (đồng bộ): initial sync (tải chain) vs catch-up.
- **Peer** (điểm ngang hàng): quản lý connections, scoring.

**Bài tập đề xuất**:
- Quan sát log: peer connections, inbound/outbound, block fetch.
- Mô phỏng slow peer hoặc partition (chia mạng – *mạng bị tách*).

---

### Giai đoạn 5 — Tooling, QA và đóng góp

**Mục tiêu**: có workflow đóng góp chuẩn.

- **CI** (Continuous Integration – *tự động build/test khi mở PR*): đọc pipeline.
- Viết test:
  - Unit test (kiểm thử đơn vị).
  - Integration test (kiểm thử tích hợp).
- Observability:
  - Log levels.
  - Metrics (đếm/gauge/histogram).

**Kết quả cần đạt**:
- Mở PR nhỏ: sửa doc, thêm test, hoặc fix bug nhỏ kèm test.

---

## 3) MVP Requirements (Yêu cầu MVP) – theo hướng “xây được thứ chạy được”

Phần này đề xuất một MVP mang tính **thực dụng** cho mina-core/stack liên quan: tạo một node/dev setup có khả năng chạy, quan sát, và cung cấp API cơ bản.

### 3.1 Phạm vi MVP

**MVP nên có**:
1) **Khởi chạy node** với cấu hình tối thiểu.
2) **Kết nối P2P** và sync (ít nhất là mode test/dev).
3) **RPC/GraphQL/API** cơ bản để:
   - Lấy status node.
   - Submit transaction.
   - Query account/ledger state.
4) **Mempool** hoạt động:
   - Nhận tx hợp lệ, từ chối tx sai (signature/nonce/fee).
5) **Block production** (nếu môi trường cho phép):
   - Tạo block trong devnet/sandbox.
6) **Logging + metrics**:
   - Log có cấu trúc (structured logging – *log dạng key/value dễ query*).
   - Export metrics (Prometheus endpoint).

**MVP không bắt buộc** (có thể để giai đoạn 2):
- Tối ưu hiệu năng cao.
- Hardening bảo mật production.
- Tính năng UX nâng cao.

---

### 3.2 Yêu cầu chức năng (Functional Requirements)

#### FR1 — Node lifecycle
- Node phải **start/stop** sạch (graceful shutdown – *tắt có xử lý dở dang*).
- Có healthcheck:
  - `ready` (sẵn sàng phục vụ).
  - `live` (đang chạy).

#### FR2 — Networking & sync
- Node có thể:
  - Add peer tĩnh (static peer).
  - Auto-discover peer (nếu có).
  - Sync header/body tối thiểu.

#### FR3 — Transaction path
- RPC endpoint để submit tx.
- Validate tx:
  - **Signature** (chữ ký).
  - **Nonce** (số thứ tự chống replay – *chống phát lại giao dịch*).
  - Balance/fee.
- Tx hợp lệ đi vào mempool.

#### FR4 — Ledger query
- Query account:
  - balance
  - nonce
  - public key
- Query chain head (đỉnh chain).

#### FR5 — Observability
- Logs:
  - Có correlation id (mã liên kết – *theo dõi một request xuyên suốt*).
- Metrics:
  - peers_connected
  - mempool_size
  - blocks_received
  - blocks_produced (nếu có)
  - rpc_request_duration

---

### 3.3 Yêu cầu phi chức năng (Non-Functional Requirements)

#### NFR1 — Reproducible build
- Build phải tái lập:
  - Build doc rõ ràng.
  - Script/Dockerfile (nếu dùng) chạy được.

#### NFR2 — Performance (mức MVP)
- Node không rò rỉ bộ nhớ nghiêm trọng.
- RPC P95 latency (độ trễ 95% – *phần lớn request*) ở mức chấp nhận được trong dev.

#### NFR3 — Security (tối thiểu)
- RPC có giới hạn truy cập:
  - bind localhost mặc định hoặc có allowlist.
- Rate limiting (giới hạn tần suất) cho submit tx.

#### NFR4 — Backward compatibility
- Thay đổi config/RPC cần versioning:
  - **SemVer** (phiên bản ngữ nghĩa – *MAJOR.MINOR.PATCH*).

---

## 4) Checklist triển khai MVP (gợi ý theo sprint)

### Sprint 1 — “Chạy được”
- [ ] Build từ source
- [ ] Chạy node với config tối thiểu
- [ ] Log startup + version info

### Sprint 2 — “Nói chuyện được”
- [ ] P2P connect peer
- [ ] Sync tối thiểu (head tip)
- [ ] Endpoint status/health

### Sprint 3 — “Gửi giao dịch được”
- [ ] RPC submit tx
- [ ] Validate tx + mempool
- [ ] Metrics mempool/tx accepted/rejected

### Sprint 4 — “Quan sát & ổn định”
- [ ] Prometheus metrics endpoint
- [ ] Basic dashboards (tùy chọn)
- [ ] Integration test cho tx path

---

## 5) Danh mục thuật ngữ (Glossary) – giải thích nhanh

- **MVP (Minimum Viable Product)**: phiên bản tối thiểu có thể vận hành để kiểm chứng.
- **PoS (Proof of Stake)**: cơ chế đồng thuận dựa trên stake.
- **zk-SNARK**: bằng chứng không tiết lộ, ngắn gọn, kiểm tra nhanh.
- **Merkle tree**: cấu trúc cây băm để chứng minh dữ liệu thuộc tập.
- **RPC**: API gọi hàm từ xa.
- **GraphQL**: dạng API truy vấn theo schema, client chọn trường cần lấy.
- **Gossip**: cơ chế lan truyền thông tin trong mạng P2P.
- **Rate limit**: giới hạn tần suất request để chống spam.
- **P95 latency**: độ trễ ở percentile 95.

---

## 6) Gợi ý đóng góp tiếp theo

- Viết thêm tài liệu “How to run devnet/sandbox” bằng tiếng Việt.
- Thêm ví dụ gọi RPC submit tx + query account.
- Tạo checklist debug thường gặp: peer không connect, sync kẹt, tx bị reject.
