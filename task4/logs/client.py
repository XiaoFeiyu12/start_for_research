"""
TCP 客户端
功能：每秒向服务端发送一个随机数（0-100）
"""

import socket
import struct
import random
import time
import sys


def main():
	if len(sys.argv) != 3:
		print("使用方法: python client.py <服务端IP> <端口>")
		print("例如: python client.py 127.0.0.1 8080")
		sys.exit(1)

	host = sys.argv[1]
	port = int(sys.argv[2])

	print(f"客户端启动，准备连接到 {host}:{port}")

	# TODO: 你的代码
	# 提示流程：
	# 1. 创建 socket 对象
	#    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#
	# 2. 连接到服务端
	#    client_socket.connect((host, port))
	#    print(f"成功连接到服务端 {host}:{port}")
	#
	# 3. 循环发送数据
	#    while True:
	#        # 3.1 生成随机数（0-100）
	#        random_num = random.randint(0, 100)
	#
	#        # 3.2 将整数打包成字节（使用 struct.pack）
	#        #     'i' 表示整数（4字节），'>' 表示大端字节序（网络字节序）
	#        data = struct.pack('>i', random_num)
	#
	#        # 3.3 发送数据
	#        client_socket.send(data)
	#        print(f"发送数据: {random_num}")
	#
	#        # 3.4 等待 1 秒
	#        time.sleep(1)
	#
	# 4. 异常处理（可选但推荐）
	#    try:
	#        ... 上面的代码 ...
	#    except KeyboardInterrupt:
	#        print("\n客户端停止")
	#    except Exception as e:
	#        print(f"错误: {e}")
	#    finally:
	#        client_socket.close()
	#        print("连接已关闭")

	try:
		client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		client_socket.connect((host,port))
		while True:
			num = random.randint(0,100)
			data = struct.pack(">i",num)
			client_socket.send(data)
			print(f"已发送数据{num}")
			time.sleep(1)
            
	except KeyboardInterrupt:
		print("\n客户端被停止")
	except Exception as e :
		print(f"客户端发生错误：{e}")
	finally:
		client_socket.close()
		print("连接已关闭")

if __name__ == '__main__':
	main()
