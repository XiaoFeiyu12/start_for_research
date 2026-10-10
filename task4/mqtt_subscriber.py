"""
MQTT 订阅者
功能：订阅 MQTT 主题，收到数据后写入文本文件（时间戳 + 数据值）

数据流：mqtt_publisher.py → MQTT Broker → 本程序 → received_data.txt
"""

# 需要导入的库：sys, paho.mqtt.client, datetime

# MQTT 配置
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "tcp/data"
OUTPUT_FILE = "received_data.txt"

# -----------------------------------------------------------------------
# 提示：整体结构
#
# 需要定义两个回调函数，然后在 main() 里把它们绑定到 client 上：
#
# 回调 1：on_connect
#   触发时机：client.connect() 成功或失败后自动调用
#   参数：(client, userdata, flags, reason_code, properties)
#   要做的事：
#     - reason_code == 0 表示连接成功，打印一下
#     - 在这里调用 client.subscribe(MQTT_TOPIC, qos=1) 订阅主题
#       （放这里的原因：断线重连后 on_connect 会再次触发，自动重新订阅）
#
# 回调 2：on_message
#   触发时机：每收到一条消息自动调用
#   参数：(client, userdata, msg)
#     - msg.payload 是 bytes，用 .decode("utf-8") 转为字符串
#     - userdata 是创建 client 时传入的自定义数据（文件路径）
#   要做的事：
#     - 获取当前时间戳（毫秒精度）：
#       datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
#       （[:-3] 把微秒6位截短为毫秒3位）
#     - 拼成一行："{timestamp},{value}\n"
#     - 以追加模式写入文件：open(文件路径, "a", encoding="utf-8")
#     - 打印收到的数据
#
# main() 要做的事：
#   - 支持命令行参数指定输出文件：sys.argv[1] if len(sys.argv) > 1 else OUTPUT_FILE
#   - 创建 client，通过 userdata 把文件路径传给回调（避免全局变量）：
#     mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata={"output_file": 文件路径})
#   - 绑定两个回调函数
#   - connect 后调用 loop_forever()（阻塞，持续等消息）
#   - try/except KeyboardInterrupt/finally，finally 里 disconnect()
# -----------------------------------------------------------------------
