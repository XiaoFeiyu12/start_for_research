"""
Web 服务器 - 提供实时数据可视化网页
功能：启动 HTTP 服务器，提供数据查询 API 和前端页面
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from database import Database


class DataHandler(BaseHTTPRequestHandler):
	# 类变量：数据库连接（所有请求共享）
	db = None

	def do_GET(self):
		"""处理 GET 请求"""
		if self.path == '/':
			# 返回主页 HTML
			self.send_response(200)
			self.send_header('Content-Type', 'text/html; charset=utf-8')
			self.end_headers()
			with open('index.html', 'rb') as f:
				self.wfile.write(f.read())

		elif self.path == '/api/data':
			# 返回最近 20 条数据（JSON 格式）
			try:
				data = DataHandler.db.get_recent_data(20)
				# 转换为 JSON 格式：[{id, timestamp, value, client}, ...]
				result = []
				for row in data:
					result.append({
						'id': row[0],
						'timestamp': str(row[1]),
						'value': row[2],
						'client': row[3]
					})

				self.send_response(200)
				self.send_header('Content-Type', 'application/json')
				self.send_header('Access-Control-Allow-Origin', '*')  # 允许跨域
				self.end_headers()
				self.wfile.write(json.dumps(result).encode())
			except Exception as e:
				self.send_error(500, f'Database error: {e}')

		else:
			self.send_error(404, 'Not Found')

	def log_message(self, format, *args):
		"""简化日志输出"""
		print(f"[Web] {self.address_string()} - {format % args}")


def start_web_server(host='0.0.0.0', port=8000, db_config=None):
	"""
	启动 Web 服务器

	参数：
		host: str - 监听地址
		port: int - 监听端口
		db_config: dict - 数据库配置 {host, user, password, database}
	"""
	# 初始化数据库连接
	if db_config is None:
		db_config = {
			'host': 'localhost',
			'user': 'xiaofeiyu12',
			'password': '123456',
			'database': 'tcp_data'
		}

	DataHandler.db = Database(**db_config)
	print(f"数据库已连接")

	# 启动 HTTP 服务器
	server = HTTPServer((host, port), DataHandler)
	print(f"Web 服务器启动: http://{host}:{port}")
	print(f"在浏览器中打开查看实时曲线")
	print(f"按 Ctrl+C 停止\n")

	try:
		server.serve_forever()
	except KeyboardInterrupt:
		print("\n\n🛑 Web 服务器停止")
		DataHandler.db.close()


if __name__ == '__main__':
	import sys

	if len(sys.argv) == 3:
		host = sys.argv[1]
		port = int(sys.argv[2])
		start_web_server(host, port)
	else:
		print("使用方法: python web_server.py <监听IP> <端口>")
		print("例如: python web_server.py 0.0.0.0 8000")
		print("\n使用默认配置启动: 0.0.0.0:8000")
		start_web_server()
