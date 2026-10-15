#!/bin/bash
# 启动所有 task5 服务，日志混合输出到当前终端，Ctrl+C 全部停止

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "TCP 服务端监听: 127.0.0.1:8080"
echo "Web API 地址:   http://localhost:8000/api/data"
echo ""

# -----------------------------------------------------------------------
# 提示：后台启动三个进程，日志直接输出到终端
#
# 每个进程后台启动（加 &），用 $! 记录 PID
#   python3 -u 强制无缓冲，日志实时输出
#
# 三个程序：
#   tcp_server.py  127.0.0.1 8080
#   web_server.py  （无参数）
#   tcp_client.py  127.0.0.1 8080
#
# 启动后用 trap 捕获 Ctrl+C（SIGINT），统一 kill 所有 PID：
#   trap "kill $SERVER_PID $WEB_PID $CLIENT_PID 2>/dev/null; exit" INT
#   （trap 必须在后台进程启动之后设置，否则 PID 变量还没有值）
#
# 最后调用 wait，让脚本阻塞在这里等三个子进程：
#   wait
#   这样 Ctrl+C 会先触发 trap，kill 掉三个进程，再退出
#
# TODO: 你的代码
if docker ps -a --format '{{.Names}}' | grep -q '^emqx$'; then
    docker start emqx
else
    docker run -d --name emqx \
      -p 1883:1883 -p 8083:8083 -p 8084:8084 \
      -p 8883:8883 -p 18083:18083 \
      docker.io/emqx/emqx-enterprise:latest
fi
sleep 5

python3 -u $SCRIPT_DIR/mqtt_subscriber.py "$SCRIPT_DIR/logs/received_data.txt" &
SUBSCRIBER_PID=$!

python3 -u $SCRIPT_DIR/mqtt_publisher.py 127.0.0.1 8080 &
PUBLISHER_PID=$!

python3 -u $SCRIPT_DIR/web_server.py &
WEB_SERVER_PID=$!
echo "网页查询：http://localhost:8000"
sleep 1

python3 -u $SCRIPT_DIR/tcp_client.py 127.0.0.1 8080 &
CLIENT_PID=$!

trap "kill $SUBSCRIBER_PID $PUBLISHER_PID $WEB_SERVER_PID $CLIENT_PID 2>/dev/null; exit" INT
wait
# -----------------------------------------------------------------------
