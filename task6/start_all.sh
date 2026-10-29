#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "TCP 服务端监听: 127.0.0.1:8080"
echo "Web API 地址:   http://localhost:8000/api/data"
echo "网页查询：http://localhost:8000"
echo ""
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

streamlit run $SCRIPT_DIR/app.py &

sleep 1

python3 -u $SCRIPT_DIR/tcp_client.py 127.0.0.1 8080 &
CLIENT_PID=$!


trap "kill $SUBSCRIBER_PID $PUBLISHER_PID $WEB_SERVER_PID $CLIENT_PID 2>/dev/null; exit" INT
wait
