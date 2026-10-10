#!/bin/bash
# 查看服务状态

cd "$(dirname "$0")"

echo "📊 服务状态检查"
echo "================================"

# 检查进程是否运行
check_process() {
    NAME=$1
    PATTERN=$2
    PID_FILE=$3

    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 $PID 2>/dev/null; then
            echo "✅ $NAME 运行中 (PID: $PID)"
            return 0
        else
            echo "❌ $NAME 已停止 (PID 文件过期)"
            return 1
        fi
    else
        # 尝试按名称查找
        PID=$(pgrep -f "$PATTERN" | head -n1)
        if [ -n "$PID" ]; then
            echo "⚠️  $NAME 运行中 (PID: $PID, 无 PID 文件)"
            return 0
        else
            echo "❌ $NAME 未运行"
            return 1
        fi
    fi
}

check_process "TCP 服务端" "python3 server.py" "logs/server.pid"
check_process "Web 服务器" "python3 web_server.py" "logs/web_server.pid"
check_process "TCP 客户端" "python3 client.py" "logs/client.pid"

echo ""
echo "🌐 端口占用情况"
echo "================================"
lsof -i :8080 2>/dev/null && echo "" || echo "8080 端口空闲"
lsof -i :8000 2>/dev/null || echo "8000 端口空闲"

echo ""
echo "📝 最近日志 (logs/server.log 最后 5 行)"
echo "================================"
if [ -f logs/server.log ]; then
    tail -n 5 logs/server.log
else
    echo "日志文件不存在"
fi
