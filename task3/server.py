"""
TCP 服务端
功能：接收客户端发送的数据，并存储到 MySQL 数据库
"""

import socket
import struct
import sys
from database import Database


def main():
	if len(sys.argv) != 3:
		print("使用方法: python server.py <监听IP> <端口>")
		print("例如: python server.py 127.0.0.1 8080")
		sys.exit(1)

	host = sys.argv[1]
	port = int(sys.argv[2])

	print(f"服务端启动，监听 {host}:{port}")

	# TODO: 你的代码
	# 提示流程：
	# 1. 初始化数据库连接
	#    db = Database(host='localhost', user='root', password='your_password', database='tcp_data')
	#    注意：记得修改密码为你的 MySQL 密码
	#
	# 2. 创建 socket 对象并设置选项
	#    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 允许端口重用
	#
	# 3. 绑定地址和端口
	#    server_socket.bind((host, port))
	#
	# 4. 开始监听（backlog=5 表示最多排队5个连接）
	#    server_socket.listen(5)
	#    print(f"开始监听，等待客户端连接...")
	#
	# 5. 接受客户端连接
	#    client_socket, client_address = server_socket.accept()
	#    print(f"客户端已连接: {client_address}")
	#
	# 6. 循环接收数据
	#    while True:
	#        # 6.1 接收 4 字节数据（一个整数）
	#        data = client_socket.recv(4)
	#
	#        # 6.2 如果没有数据，说明连接断开
	#        if not data:
	#            print("客户端断开连接")
	#            break
	#
	#        # 6.3 解包数据（从字节转换为整数）
	#        #     'i' 表示整数，'>' 表示大端字节序
	#        received_value = struct.unpack('>i', data)[0]
	#
	#        # 6.4 构造客户端地址字符串
	#        client_addr_str = f"{client_address[0]}:{client_address[1]}"
	#
	#        # 6.5 存入数据库
	#        success = db.insert_data(received_value, client_addr_str)
	#
	#        # 6.6 打印接收到的数据
	#        if success:
	#            print(f"接收数据: {received_value} | 来自: {client_addr_str} | 已存入数据库")
	#        else:
	#            print(f"接收数据: {received_value} | 来自: {client_addr_str} | 数据库插入失败")
	#
	# 7. 异常处理和资源清理
	#    try:
	#        ... 上面的代码 ...
	#    except KeyboardInterrupt:
	#        print("\n服务端停止")
	#    except Exception as e:
	#        print(f"错误: {e}")
	#    finally:
	#        client_socket.close()
	#        server_socket.close()
	#        db.close()
	#        print("连接已关闭，数据库已断开")

	try:
		db = Database("localhost",'xiaofeiyu12','123456','tcp_data')
		server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind((host,port))
		server_socket.listen()
		print("服务端监听中...")
		client_socket, client_addr = server_socket.accept()
		print(f"已接收客户端:{client_addr}")
		while True:
			data = client_socket.recv(4)
			if not data:
				print("未接受到数据，客户端连接已断开")
				break
			num = struct.unpack(">i",data)[0]
			client_addr_str = f"{client_addr[0]}:{client_addr[1]}"
			success = db.insert_data(num,client_addr_str)
			if success:
				print(f"接收数据: {num} | 来自: {client_addr_str} | 已存入数据库")
			else:
				print(f"接收数据: {num} | 来自: {client_addr_str} | 数据库插入失败")
	except KeyboardInterrupt:
		print("\n服务端被停止")
	except Exception as e:
		print(f"服务端错误：{e}")
	finally:
		db.close()
		print("连接已关闭，数据库已断开")


if __name__ == '__main__':
	main()
