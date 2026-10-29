"""
数据库操作封装类
功能：连接 MySQL 数据库，插入和查询 TCP 接收到的数据
"""

import mysql.connector
from datetime import datetime
from tools.logger import Logger

# 数据库配置
DB_HOST = "localhost"
DB_USER = "xiaofeiyu12"
DB_PASSWORD = "123456"
DB_NAME = "tcp_data"


class Database:
	def __init__(self, host='localhost', user='root', password='your_password', database='tcp_data'):
		"""
		初始化数据库连接

		TODO: 你的代码
		提示：
		1. 使用 mysql.connector.connect() 创建连接
		2. 保存连接对象到 self.conn
		3. 创建游标对象保存到 self.cursor
		4. 添加 try-except 处理连接失败的情况
		"""
		try:
			self.conn = mysql.connector.connect(
				host=host,
				user=user,
				password=password,
				database=database,
				autocommit=True  # 自动提交，确保读取到最新数据
			)
			self.logger = Logger(database,"logs/database.log")
			self.logger.info(f"数据库连接成功: {database}")
			
		except mysql.connector.Error as e:
			self.logger.error(f"数据库连接失败: {e}")
			raise  # 重新抛出异常，让调用者知道连接失败


	def insert_data(self, data_value, client_address):
		"""
		插入一条数据到数据库

		参数：
			data_value: int - 接收到的数据值
			client_address: str - 客户端地址，格式 "IP:Port"

		返回：
			bool - 插入是否成功

		TODO: 你的代码
		提示：
		1. SQL 语句：INSERT INTO received_data (data_value, client_address) VALUES (%s, %s)
		2. 使用 self.cursor.execute(sql, (data_value, client_address))
		3. 使用 self.conn.commit() 提交事务
		4. 添加 try-except 处理插入失败的情况
		5. 返回 True 表示成功，False 表示失败
		"""
		try:
			cursor = self.conn.cursor()
			sql_command = f"INSERT INTO received_data (data_value, client_address) VALUES (%s, %s)"
			cursor.execute(sql_command, (data_value, client_address))
			self.logger.debug(f"插入数据:{data_value}|{client_address}")
			cursor.close()
			return True
		except mysql.connector.Error as e:
			self.logger.error(f"插入数据失败:{e}")
			return False

	def get_recent_data(self, limit=10):
		"""
		查询最近 N 条数据

		参数：
			limit: int - 查询数量，默认 10

		返回：
			list - 查询结果列表，每个元素是一个元组 (id, timestamp, data_value, client_address)

		TODO: 你的代码
		提示：
		1. SQL 语句：SELECT * FROM received_data ORDER BY timestamp DESC LIMIT %s
		2. 使用 self.cursor.execute(sql, (limit,))
		3. 使用 self.cursor.fetchall() 获取结果
		4. 添加 try-except 处理查询失败的情况
		"""
		try:
			cursor = self.conn.cursor()
			sql_command = f"SELECT * FROM received_data ORDER BY timestamp DESC LIMIT %s"
			cursor.execute(sql_command, (limit,))
			result = cursor.fetchall()
			cursor.close()
			return result
		except mysql.connector.Error as e:
			self.logger.error(f"数据查询失败: {e}")
			return []  # 查询失败返回空列表
		

	def get_data_by_time_range(self, start, end):
		"""
		查询某个时间段内的数据

		参数：
			start: str - 开始时间，格式 "YYYY-MM-DD HH:MM:SS"
			end:   str - 结束时间，格式 "YYYY-MM-DD HH:MM:SS"

		返回：
			list - 查询结果列表，每个元素是一个元组 (id, timestamp, data_value, client_address)

		提示：
		- SQL 语句：SELECT * FROM received_data WHERE timestamp BETWEEN %s AND %s ORDER BY timestamp ASC
		- BETWEEN 是闭区间，包含两端
		- 参数传 (start, end) 元组，不要用 f-string 拼 SQL（防 SQL 注入）
		- 结构参考 get_recent_data()

		TODO: 你的代码
		"""
		try:
			cursor = self.conn.cursor()
			sql_command = f"SELECT * FROM received_data WHERE timestamp BETWEEN %s AND %s ORDER BY timestamp ASC"
			cursor.execute(sql_command, (start,end))
			result = cursor.fetchall()
			cursor.close()
			return result
		except mysql.connector.Error as e:
			self.logger.error(f"数据查询失败: {e}")
			return []  # 查询失败返回空列表

	def close(self):
		"""
		关闭数据库连接

		TODO: 你的代码
		提示：
		1. 关闭游标：self.cursor.close()
		2. 关闭连接：self.conn.close()
		3. 添加 try-except 确保资源释放
		"""
		try:
			if self.conn:
				self.conn.close()
			self.logger.info("数据库连接已关闭")
		except mysql.connector.Error as e:
			self.logger.error(f"关闭连接时出错: {e}")


# 测试代码（可选）
if __name__ == '__main__':
	# 测试数据库连接和操作
	db = Database(host='localhost', user='xiaofeiyu12', password='123456', database='tcp_data')

	# 测试插入
	success = db.insert_data(42, '127.0.0.1:12345')
	print(f"插入{'成功' if success else '失败'}")

	# 测试查询
	results = db.get_recent_data(5)
	print(f"最近 5 条数据：")
	for row in results:
		print(f"  ID: {row[0]}, 时间: {row[1]}, 数据: {row[2]}, 客户端: {row[3]}")

	# 关闭连接
	db.close()
