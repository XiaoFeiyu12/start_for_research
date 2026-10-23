"""
MQTT 订阅者
功能：订阅 MQTT 主题，收到数据后写入文本文件（时间戳 + 数据值）

数据流：mqtt_publisher.py → MQTT Broker → 本程序 → received_data.txt
"""

# 需要导入的库：sys, paho.mqtt.client, datetime
import sys
import paho.mqtt.client as mqtt
import datetime
from tools.logger import Logger
from database import Database

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "tcp/data"
OUTPUT_FILE = "received_data.txt"

# -----------------------------------------------------------------------
# 提示：用类封装
#
# 类名：MqttSubscriber
#
# __init__(self, broker, port, topic, output_file)
#   - 保存所有参数到实例变量
#   - 初始化 self.client = None
#
# _on_connect(self, client, userdata, flags, reason_code, properties)
#   - reason_code == 0 时打印连接成功
#   - 在这里调用 client.subscribe(self.topic, qos=1)
#     （放这里是因为断线重连后会再次触发，自动重新订阅）
#
# _on_message(self, client, userdata, msg)
#   - msg.payload.decode("utf-8") 得到数据字符串
#   - datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] 得到毫秒时间戳
#   - 拼成 "{timestamp},{value}\n" 追加写入 self.output_file
#   - 打印收到的数据
#
# start(self)
#   - 创建 mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
#   - 绑定 self._on_connect 和 self._on_message
#     （不需要 userdata 了，直接用 self.output_file）
#   - connect 后调用 loop_forever()（阻塞，持续等消息）
#
# stop(self)
#   - client.disconnect()
#
# main() 函数：
#   - 支持命令行参数指定输出文件：sys.argv[1] if len(sys.argv) > 1 else OUTPUT_FILE
#   - 创建 MqttSubscriber 实例，调用 start()
#   - try/except KeyboardInterrupt/finally，finally 里调用 stop()
# -----------------------------------------------------------------------
class MqttSubscription:
    def __init__(self,broker,port,topic,userdata,name="MqttSubscription"):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.userdata = userdata
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            userdata=self.userdata)
        self.logger = Logger(name,"logs/mqtt_subscription.log")

        self.client.on_connect = self.__on_connect__
        self.client.on_message = self.__on_message__


    def __on_connect__(self,client,userdata,flags,reason_code,properties):
        if(reason_code == 0):
            self.logger.info("连接broker成功")
            client.subscribe(self.topic,qos=1)
            return True
        else:
            self.logger.warning("连接失败")
            return False

    def __on_message__(self,client,userdata,msg):
        data=msg.payload.decode("utf-8")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        with open(userdata["output_file"],"a",encoding="utf-8",newline="") as f:
            f.write(f"[{timestamp}]:{data}\n")      
        self.logger.debug(f"收到数据{data}")

    def start(self):
        self.logger.info("正在连接中...")
        self.client.connect(
            host=self.broker,
            port=self.port
        )
        self.client.loop_forever()

    def stop(self):
        self.logger.info("已关闭")
        self.client.disconnect()

if __name__ == "__main__":
    try:
        output_file = sys.argv[1] if len(sys.argv)>1 else OUTPUT_FILE
        userdata = {"output_file":output_file}
        subscription = MqttSubscription(MQTT_BROKER,MQTT_PORT,MQTT_TOPIC,userdata)
        subscription.start()
    except KeyboardInterrupt:
        subscription.logger.info("用户Ctrl+C打断进程")
    except Exception as e:
        subscription.logger.error(f"错误: {e}")
    finally:
        subscription.stop()
