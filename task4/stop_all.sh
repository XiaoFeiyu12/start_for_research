#!/bin/bash
# 停止所有 task4 服务

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"

echo "=== Task4 停止 ==="

stop_process() {
	local name=$1
	local pid_file="$LOG_DIR/${name}.pid"
	if [ -f "$pid_file" ]; then
		pid=$(cat "$pid_file")
		if kill -0 "$pid" 2>/dev/null; then
			kill "$pid"
			echo "[$name] 已停止 (pid=$pid)"
		else
			echo "[$name] 进程不存在 (pid=$pid)"
		fi
		rm -f "$pid_file"
	else
		echo "[$name] 未找到 pid 文件"
	fi
}

stop_process publisher
stop_process subscriber

echo ""
echo "EMQX 容器保持运行，如需停止："
echo "  docker stop emqx"
