"""
TCP 客户端
功能：每秒向服务端发送一个随机数（0-100）
"""

import socket
import struct
import random
import time
import sys
from datetime import datetime
from tools.logger import Logger


class TcpClient:
    def __init__(self, host, port,name="TcpClient"):
        self.host = host
        self.port = port
        self.socket = None
        self.logger = Logger(name=name)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))
        self.logger.log_info(f"已连接到 {self.host}:{self.port}")

    def run(self):
        while True:
            num = random.randint(0,100)
            data = struct.pack(">i", num)
            self.socket.send(data)
            self.logger.log_info(f"已发送数据: {num}")
            time.sleep(1)

    def close(self):
        if self.socket:
            self.socket.close()
            self.logger.log_info(f"连接已关闭")


def main():
    if len(sys.argv) != 3:
        print("使用方法: python tcp_client.py <服务端IP> <端口>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    client = TcpClient(host, port)
    try:
        client.connect()
        client.run()
    except KeyboardInterrupt:
        print(f"\n:客户端停止")
    except Exception as e:
        print(f"错误: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
