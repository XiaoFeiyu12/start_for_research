#!/bin/bash
# 启动所有服务（后台运行）

cd "$(dirname "$0")"

echo "🚀 启动服务..."

# 启动 TCP 服务端
python3 server.py 127.0.0.1 8080 > logs/server.log 2>&1 &
SERVER_PID=$!
echo "✓ TCP 服务端已启动 (PID: $SERVER_PID)"

# 等待服务端启动
sleep 1

# 启动 Web 服务器
python3 web_server.py 0.0.0.0 8000 > logs/web_server.log 2>&1 &
WEB_PID=$!
echo "✓ Web 服务器已启动 (PID: $WEB_PID)"

# 启动 TCP 客户端
python3 client.py 127.0.0.1 8080 > logs/client.log 2>&1 &
CLIENT_PID=$!
echo "✓ TCP 客户端已启动 (PID: $CLIENT_PID)"

# 保存 PID 到文件
mkdir -p logs
echo $SERVER_PID > logs/server.pid
echo $WEB_PID > logs/web_server.pid
echo $CLIENT_PID > logs/client.pid

echo ""
echo "✅ 所有服务已启动"
echo "📊 打开浏览器访问: http://localhost:8000"
echo "📝 日志目录: logs/"
echo "🛑 停止服务: ./stop_all.sh"
