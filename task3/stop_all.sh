#!/bin/bash
# 停止所有服务

cd "$(dirname "$0")"

echo "🛑 停止服务..."

# 从 PID 文件读取并杀进程
if [ -f logs/server.pid ]; then
    SERVER_PID=$(cat logs/server.pid)
    if kill -0 $SERVER_PID 2>/dev/null; then
        kill $SERVER_PID
        echo "✓ TCP 服务端已停止 (PID: $SERVER_PID)"
    fi
    rm logs/server.pid
fi

if [ -f logs/web_server.pid ]; then
    WEB_PID=$(cat logs/web_server.pid)
    if kill -0 $WEB_PID 2>/dev/null; then
        kill $WEB_PID
        echo "✓ Web 服务器已停止 (PID: $WEB_PID)"
    fi
    rm logs/web_server.pid
fi

if [ -f logs/client.pid ]; then
    CLIENT_PID=$(cat logs/client.pid)
    if kill -0 $CLIENT_PID 2>/dev/null; then
        kill $CLIENT_PID
        echo "✓ TCP 客户端已停止 (PID: $CLIENT_PID)"
    fi
    rm logs/client.pid
fi

# 兜底：按名称杀进程（防止 PID 文件丢失）
pkill -f "python3 server.py" 2>/dev/null
pkill -f "python3 web_server.py" 2>/dev/null
pkill -f "python3 client.py" 2>/dev/null

echo "✅ 所有服务已停止"
