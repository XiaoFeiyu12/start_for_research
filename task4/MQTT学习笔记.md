# MQTT 知识点学习文档

## 1. MQTT 是什么

MQTT（Message Queuing Telemetry Transport）是一个**发布/订阅**消息协议，专为低带宽、不稳定网络设计。现在是物联网（IoT）的标准协议，ROS2 的话题机制和它的思想非常相似。

---

## 2. 与 TCP 的本质区别

TCP 是**点对点**通信，发送方必须直接连接接收方：

```
TCP Client ──直连──► TCP Server
```

MQTT 是**发布/订阅**，双方不直接连接，通过 Broker（代理）解耦：

```
Publisher ──发布──► Broker ──推送──► Subscriber A
           主题                      Subscriber B
                                     Subscriber C
```

类比 ROS2：
- MQTT Broker ≈ ROS2 的 DDS 中间层
- MQTT Topic ≈ ROS2 Topic
- Publisher/Subscriber ≈ ROS2 的 publisher/subscriber 节点

| 对比项 | TCP | MQTT |
|--------|-----|------|
| 通信方式 | 点对点，需要知道对方 IP | 都连 Broker，互不知道对方 |
| 耦合度 | 强（发送方必须等接收方在线） | 解耦（Broker 可缓存消息） |
| 一对多 | 需要自己写广播逻辑 | 天然支持 |
| 断线处理 | 消息丢失 | QoS 机制可保证送达 |

---

## 3. 核心概念

### Broker（代理服务器）
消息中转站，所有客户端都连它，它负责接收和分发消息。本任务用 EMQX 搭建。

### Topic（主题）
消息的"频道"，字符串格式，用 `/` 分层：
```
tcp/data
sensors/room1/temperature
robot/arm/position
```

支持通配符订阅：
- `+` — 匹配单层，例如 `sensors/+/temperature` 匹配 `sensors/room1/temperature`
- `#` — 匹配多层，例如 `sensors/#` 匹配所有传感器主题

### QoS（服务质量）
消息送达保证级别：

| QoS | 含义 | 适用场景 |
|-----|------|----------|
| 0 | 最多送达一次（可能丢） | 传感器高频数据，丢一条无所谓 |
| 1 | 至少送达一次（可能重复） | 本任务使用，一般场景的推荐值 |
| 2 | 恰好送达一次（最可靠最慢） | 支付、指令等不能重复的场景 |

### Retain（保留消息）
发布时设置 `retain=True`，Broker 会保存最后一条消息。新订阅者连接后立即收到最新值，不用等下一次发布。适合状态类数据（如设备当前状态）。

---

## 4. paho-mqtt 库使用

### 安装
```bash
pip3 install paho-mqtt
```

### 创建客户端
```python
import paho.mqtt.client as mqtt

# paho-mqtt 2.x 必须指定 CallbackAPIVersion
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
```

### 回调函数（事件驱动）

paho-mqtt 是事件驱动的，你定义函数，库在事件发生时自动调用：

```python
# 连接成功/失败时触发
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("连接成功")
        # 通常在这里订阅主题，因为重连后会再次触发
        client.subscribe("tcp/data", qos=1)

# 收到消息时触发（订阅者用）
def on_message(client, userdata, msg):
    value = msg.payload.decode("utf-8")  # bytes → str
    topic = msg.topic

# 消息发布成功确认时触发（发布者可选）
def on_publish(client, userdata, mid, reason_code, properties):
    pass  # mid 是消息 ID

# 绑定到 client
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
```

### userdata — 向回调传递数据

不用全局变量，通过 `userdata` 把数据传进回调：

```python
client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    userdata={"output_file": "data.txt", "count": 0}
)

def on_message(client, userdata, msg):
    output_file = userdata["output_file"]  # 在回调里取出
```

### 连接与循环

**发布者**（主线程还要做别的事，用后台循环）：
```python
client.connect("localhost", 1883, keepalive=60)
client.loop_start()    # 启动后台线程处理网络，不阻塞

# 主线程继续做 TCP 服务端的事...
client.publish("tcp/data", "42", qos=1)

# 结束时
client.loop_stop()
client.disconnect()
```

**订阅者**（只需等消息，用阻塞循环）：
```python
client.connect("localhost", 1883, keepalive=60)
client.loop_forever()  # 阻塞，直到 Ctrl+C 或 client.disconnect()
```

### 发布消息
```python
# payload 可以是 str、bytes 或数字
client.publish(topic, payload, qos=1, retain=False)
```

### 订阅主题
```python
client.subscribe("tcp/data", qos=1)
client.subscribe([("tcp/data", 1), ("tcp/status", 0)])  # 订阅多个
```

---

## 5. EMQX 搭建（Docker）

```bash
# 拉取镜像
docker pull emqx/emqx:latest

# 启动容器
docker run -d --name emqx \
  -p 1883:1883 \     # MQTT 标准端口
  -p 8083:8083 \     # MQTT over WebSocket
  -p 18083:18083 \   # Web 管理控制台
  emqx/emqx:latest

# 查看是否启动
docker ps | grep emqx

# 停止 / 重启
docker stop emqx
docker start emqx
```

Web 控制台：`http://localhost:18083`，默认账号 `admin`，密码 `public`。
可以实时查看连接的客户端、订阅的主题、消息收发统计，调试非常方便。

---

## 6. 本任务数据流

```
task3/client.py
    │  TCP，大端4字节整型
    ▼
mqtt_publisher.py（TCP 服务端）
    │  MQTT publish，主题 tcp/data，payload 为数字字符串
    ▼
EMQX Broker（localhost:1883）
    │  MQTT 推送
    ▼
mqtt_subscriber.py
    │  写文件
    ▼
received_data.txt
    格式：2026-10-10 10:23:01.123,42
          时间戳（毫秒精度）,数据值
```

---

## 7. 常见问题

**Q: 订阅者先启动还是发布者先启动？**
先启动订阅者，否则发布者已经发完消息时订阅者还没连上，消息会丢失（QoS=0/1 时）。

**Q: `loop_start()` 和 `loop_forever()` 的区别？**
`loop_start()` 在后台启动一个线程处理网络 I/O，主线程可以继续执行其他代码（发布者用）。
`loop_forever()` 阻塞当前线程，一直等消息（订阅者用）。

**Q: 为什么在 `on_connect` 里订阅，而不是在 `connect()` 之后直接订阅？**
因为网络断开后重连时，`on_connect` 会再次触发，订阅会自动恢复。如果放在外面，重连后就丢失订阅了。

**Q: `reason_code == 0` 是什么意思？**
paho-mqtt 2.x 中，`reason_code` 是一个对象，`== 0` 表示连接成功（返回码为 0x00 SUCCESS）。
