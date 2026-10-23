"""
MQTT 发布者（基于 TCP 服务端）
功能：接收 TCP 客户端发送的数据，通过 MQTT 发布到 Broker

数据流：client.py → 本程序 → MQTT Broker → mqtt_subscriber.py
"""

# 需要导入的库：socket, struct, sys, paho.mqtt.client
import socket
import struct
import sys
import paho.mqtt.client as mqtt
from tools.logger import Logger
from database import Database , DB_HOST,DB_NAME,DB_PASSWORD,DB_USER

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "tcp/data"


# -----------------------------------------------------------------------
# 提示：用类封装
#
# 类名：MqttPublisher
#
# __init__(self, tcp_host, tcp_port, mqtt_broker, mqtt_port, topic)
#   - 保存所有参数到实例变量
#   - 初始化 self.mqtt_client = None，self.server_socket = None
#
# _on_connect(self, client, userdata, flags, reason_code, properties)
#   - 绑定为实例方法，reason_code == 0 时打印连接成功
#   - 回调绑定方式：self.mqtt_client.on_connect = self._on_connect
#     （self 会自动传入，paho 不关心多出来的 self 参数）
#
# _setup_mqtt(self)
#   - 创建 mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
#   - 绑定 on_connect 回调
#   - connect 后调用 loop_start()（后台线程，不阻塞 TCP 服务端循环）
#
# _setup_tcp(self)
#   - 创建 TCP server socket，setsockopt SO_REUSEADDR，bind，listen
#
# run(self)
#   - 调用 _setup_mqtt() 和 _setup_tcp()
#   - 外层 while True：accept 新客户端连接
#   - 内层 while True：recv(4)，unpack，publish(topic, str(value), qos=1)
#   - try/except KeyboardInterrupt/finally，finally 里调用 close()
#
# close(self)
#   - 关闭 server_socket
#   - mqtt_client.loop_stop()，mqtt_client.disconnect()
#
# main() 函数：
#   - 解析命令行参数（tcp host、tcp port）
#   - 创建 MqttPublisher 实例，调用 run()
# -----------------------------------------------------------------------
class MqttPublisher:
    def __init__(
        self, broker, mqtt_port, topic, userdata, host, tcp_port, name="MqttPublisher"
    ):
        self.broker = broker
        self.mqtt_port = mqtt_port
        self.topic = topic
        self.userdata = userdata
        self.host = host
        self.tcp_port = tcp_port

        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mqtt_publisher = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2, userdata=self.userdata
        )
        self.mqtt_publisher.on_connect = self.__on_connect__

        self.logger = Logger(name,"logs/mqtt_publisher.log")

        self.db = Database(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME)

    def __on_connect__(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            self.logger.info("连接broker成功")
            return True
        else:
            self.logger.info("连接失败")
            return False

    def __setup_tcp__(self):
        self.tcp_server_socket.bind((self.host, self.tcp_port))
        self.tcp_server_socket.listen()
        
    def __setup_mqtt__(self):
        self.logger.info("正在连接话题中...")
        self.mqtt_publisher.connect(host=self.broker, port=self.mqtt_port)
        self.mqtt_publisher.loop_start()

    def run(self):
        self.__setup_mqtt__()
        self.__setup_tcp__()

        tcp_client_socket, tcp_client_addr = self.tcp_server_socket.accept()
        while True:
            data = tcp_client_socket.recv(4)
            if not data:
                self.logger.info("未接受到数据，客户端连接已断开")
                break
            num = struct.unpack(">i", data)[0]
            client_addr_str = f"{tcp_client_addr[0]}:{tcp_client_addr[1]}"
            self.db.insert_data(num,client_addr_str)
            self.mqtt_publisher.publish(self.topic,str(num),qos=1)

    def close(self):
        self.tcp_server_socket.close()
        self.mqtt_publisher.loop_stop()
        self.mqtt_publisher.disconnect()
        self.logger.info(f"所有连接已关闭")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法: python mqtt_publisher.py <服务端IP> <端口>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    mqtt_publisher = MqttPublisher(MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, None, host, port)
    try:
        mqtt_publisher.run()
    except KeyboardInterrupt:
        mqtt_publisher.logger.info("客户端停止")
    except Exception as e:
        mqtt_publisher.logger.error(f"错误: {e}")
    finally:
        mqtt_publisher.close()
