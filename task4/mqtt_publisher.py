"""
MQTT 发布者（基于 TCP 服务端）
功能：接收 TCP 客户端发送的数据，通过 MQTT 发布到 Broker

数据流：TCP Client → 本程序 → MQTT Broker → mqtt_subscriber.py
"""

# 需要导入的库：socket, struct, sys, paho.mqtt.client

# MQTT 配置（直接用这些常量）
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "tcp/data"

# -----------------------------------------------------------------------
# 提示：整体结构
#
# main() 里做两件事：
#   1. 创建 MQTT 客户端并连接 Broker，启动后台网络循环（loop_start）
#   2. 创建 TCP 服务端 socket，循环接受客户端连接，接收数据后 publish 出去
#
# MQTT 客户端怎么创建：
#   import paho.mqtt.client as mqtt
#   client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
#   绑定两个回调再 connect：
#     on_connect(client, userdata, flags, reason_code, properties)
#       → reason_code == 0 表示连接成功，打印一下
#     on_publish(client, userdata, mid, reason_code, properties)
#       → 可以只打印"消息已发布"，也可以不绑定
#   client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
#   client.loop_start()   ← 后台线程，不阻塞主线程
#
# TCP 服务端怎么写：
#   参考 task3/server.py
#   区别：不写数据库，改成 client.publish(MQTT_TOPIC, str(value), qos=1)
#   外层 while True 循环持续接受新连接（支持多个客户端轮流连）
#
# 收尾：
#   try/except KeyboardInterrupt/finally
#   finally 里：server_socket.close(), client.loop_stop(), client.disconnect()
# -----------------------------------------------------------------------
