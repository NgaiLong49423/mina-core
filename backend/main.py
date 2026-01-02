"""Mina core - minimal runnable entrypoint.

Phiên bản này là một entrypoint đơn giản để bạn có thể chạy và kiểm tra
server nhỏ phục vụ endpoint kiểm tra (health). Tất cả chú thích bên dưới
được viết bằng tiếng Việt để người mới học có thể theo dõi.

Endpoints hỗ trợ:
  - GET /       : trả về một chuỗi văn bản đơn giản (greeting)
  - GET /health : trả về JSON {"status":"ok"}

Chạy ví dụ:
  python backend/main.py --serve --port 8000
"""

# Thư viện chuẩn của Python để tạo HTTP server đơn giản
from http.server import HTTPServer, BaseHTTPRequestHandler
# Thư viện để mã hoá/giải mã JSON
import json
# Thư viện để phân tích tham số dòng lệnh
import argparse


class MinaHandler(BaseHTTPRequestHandler):
	# Hàm tiện ích để gửi phản hồi JSON
	def _send_json(self, payload, status=200):
		# json.dumps chuyển dict -> chuỗi JSON
		data = json.dumps(payload).encode("utf-8")  # encode thành bytes
		self.send_response(status)  # gửi mã trạng thái HTTP
		# header Content-Type thông báo dữ liệu trả về là JSON
		self.send_header("Content-Type", "application/json; charset=utf-8")
		# header Content-Length là độ dài dữ liệu (bắt buộc tốt để client biết)
		self.send_header("Content-Length", str(len(data)))
		self.end_headers()  # kết thúc phần header
		self.wfile.write(data)  # ghi body (bytes) vào socket

	# Xử lý các yêu cầu GET
	def do_GET(self):
		# Khi client truy cập đường gốc /
		if self.path == "/":
			text = "Mina core running\n"  # chuỗi trả về
			data = text.encode("utf-8")  # chuyển thành bytes
			self.send_response(200)  # mã HTTP 200 OK
			# Gửi header báo là plain text
			self.send_header("Content-Type", "text/plain; charset=utf-8")
			self.send_header("Content-Length", str(len(data)))
			self.end_headers()
			self.wfile.write(data)  # gửi body
		# Khi client truy cập /health trả về JSON trạng thái
		elif self.path == "/health":
			# Sử dụng hàm helper để gửi JSON {"status":"ok"}
			self._send_json({"status": "ok"})
		else:
			# Nếu đường dẫn không khớp, trả 404
			self.send_response(404)
			self.end_headers()


def run_server(host: str, port: int):
	# Tạo HTTPServer với MinaHandler để xử lý request
	server = HTTPServer((host, port), MinaHandler)
	# In thông báo để biết server đã khởi động
	print(f"Mina core starting on http://{host}:{port}")
	try:
		server.serve_forever()  # vòng lặp nhận và xử lý request liên tục
	except KeyboardInterrupt:
		# Bắt Ctrl+C để dừng server một cách gọn gàng
		print("Shutting down Mina core...")
		server.server_close()  # đóng socket


def main():
	# Parser cho tham số dòng lệnh (ví dụ --serve --port)
	parser = argparse.ArgumentParser(prog="mina-core")
	# --serve: nếu có, server sẽ chạy; nếu không, chỉ in hướng dẫn
	parser.add_argument("--serve", action="store_true", help="Start a tiny HTTP server for health checks")
	# --host: host để bind (mặc định 0.0.0.0 = mọi giao diện)
	parser.add_argument("--host", default="0.0.0.0", help="Host to bind the server to")
	# --port: cổng lắng nghe (mặc định 8000)
	parser.add_argument("--port", type=int, default=8000, help="Port to listen on")
	args = parser.parse_args()  # đọc tham số

	# Nếu người dùng yêu cầu chạy server
	if args.serve:
		run_server(args.host, args.port)  # khởi chạy server
	else:
		# Nếu không có --serve, in hướng dẫn sử dụng nhanh
		print("Mina core - placeholder entrypoint.")
		print("Run with --serve to start a simple HTTP health endpoint:")
		print("  python backend/main.py --serve --port 8000")


if __name__ == "__main__":
	# Điểm vào khi chạy file này trực tiếp: gọi main()
	main()
