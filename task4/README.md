# Task4 — MQTT 通信

在 Task3（TCP → 数据库 → Web）的基础上，引入 MQTT 通信协议。

数据流：
```
TCP Client → mqtt_publisher.py → EMQX Broker → mqtt_subscriber.py → received_data.txt
```

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `mqtt_publisher.py` | TCP 服务端 + MQTT 发布者，接收 TCP 数据后发布到 Broker |
| `mqtt_subscriber.py` | MQTT 订阅者，收到消息后写入文本文件 |
| `requirements.txt` | Python 依赖（paho-mqtt） |
| `start_all.sh` | 一键启动 EMQX + 两个程序 |
| `stop_all.sh` | 停止两个 Python 程序 |
| `received_data.txt` | 订阅者写入的数据文件（运行后生成） |

---

## 环境准备

### 1. 安装 Python 依赖

```bash
pip3 install -r requirements.txt
```

### 2. 搭建 EMQX MQTT Broker（用 Docker）

```bash
docker pull emqx/emqx:latest

docker run -d --name emqx \
  -p 1883:1883 \    # MQTT 标准端口
  -p 8083:8083 \    # MQTT over WebSocket
  -p 18083:18083 \  # Web 控制台
  emqx/emqx:latest
```

验证是否启动成功：

```bash
docker ps | grep emqx
# 浏览器访问 http://localhost:18083，账号 admin，密码 public
```

---

## 运行步骤

打开 3 个终端：

**终端 1 — 启动订阅者（先启动，否则会漏消息）**
```bash
cd task4
python3 mqtt_subscriber.py received_data.txt
```

**终端 2 — 启动发布者（TCP 服务端）**
```bash
cd task4
python3 mqtt_publisher.py 127.0.0.1 8080
```

**终端 3 — 启动 TCP 客户端发送测试数据**
```bash
cd task3
python3 client.py 127.0.0.1 8080
```

运行后查看写入的数据文件：
```bash
cat task4/received_data.txt
# 输出示例：
# 2026-10-10 10:23:01.123,42
# 2026-10-10 10:23:02.456,43
```

---

## 一键启动（可选）

```bash
cd task4
chmod +x start_all.sh stop_all.sh
./start_all.sh
# 停止：./stop_all.sh
```

---

## EMQX 管理控制台

访问 `http://localhost:18083`，默认账号 `admin`，密码 `public`。

可在控制台实时查看：
- 当前连接的客户端
- 订阅的主题列表
- 消息收发统计
