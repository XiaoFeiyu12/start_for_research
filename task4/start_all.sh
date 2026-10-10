#!/bin/bash
# 启动所有 task4 服务
# 顺序：EMQX Broker → MQTT 订阅者 → MQTT 发布者（TCP 服务端）

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"

echo "=== Task4 启动 ==="

# -----------------------------------------------------------------------
# 步骤 1：检查 EMQX 是否已在运行，没有就启动
#
# 提示：
#   docker ps --format '{{.Names}}' 列出所有运行中容器的名字
#   grep -q '^emqx$' 静默检查是否有名为 emqx 的容器（-q 不输出，只返回退出码）
#   if ! 命令; then ... fi  表示"如果命令失败（返回非0）就执行 then 块"
#
#   docker run 参数说明：
#     -d             后台运行
#     --name emqx    给容器命名，之后可以用名字代替容器 ID
#     -p 宿主端口:容器端口  端口映射
#       1883:1883    MQTT 标准端口
#       18083:18083  Web 管理控制台
#     最后是镜像名：emqx/emqx:latest
#
#   启动后 sleep 5，等 Broker 就绪，否则客户端连接会失败
#
# TODO: 你的代码
# -----------------------------------------------------------------------

echo "[1/3] 检查/启动 EMQX..."

# -----------------------------------------------------------------------
# 步骤 2：后台启动 MQTT 订阅者，日志写入 logs/subscriber.log
#
# 提示：
#   nohup 命令 > 日志文件 2>&1 &
#     nohup    让程序在终端关闭后继续运行
#     2>&1     把标准错误重定向到标准输出（合并到同一个日志文件）
#     &        放到后台运行
#   echo $! > pid文件    $! 是最后一个后台进程的 PID，保存下来方便后面 stop
#   sleep 1   稍等一下让进程完成初始化再继续
#
#   订阅者命令：python3 "$SCRIPT_DIR/mqtt_subscriber.py" "$SCRIPT_DIR/received_data.txt"
#   日志文件：  "$LOG_DIR/subscriber.log"
#   PID 文件：  "$LOG_DIR/subscriber.pid"
#
# TODO: 你的代码
# -----------------------------------------------------------------------

echo "[2/3] 启动 MQTT 订阅者..."

# -----------------------------------------------------------------------
# 步骤 3：后台启动 MQTT 发布者（TCP 服务端），方式同步骤 2
#
#   发布者命令：python3 "$SCRIPT_DIR/mqtt_publisher.py" 127.0.0.1 8080
#   日志文件：  "$LOG_DIR/publisher.log"
#   PID 文件：  "$LOG_DIR/publisher.pid"
#
# TODO: 你的代码
# -----------------------------------------------------------------------

echo "[3/3] 启动 MQTT 发布者（TCP 服务端）..."

echo ""
echo "=== 所有服务已启动 ==="
echo "TCP 服务端监听: 127.0.0.1:8080"
echo "MQTT Broker:    localhost:1883"
echo "EMQX 控制台:    http://localhost:18083  (账号 admin / 密码 public)"
echo "数据输出文件:   $SCRIPT_DIR/received_data.txt"
echo ""
echo "发送测试数据（另开终端）："
echo "  python3 ../task3/client.py 127.0.0.1 8080"
echo ""
echo "查看日志："
echo "  tail -f $LOG_DIR/publisher.log"
echo "  tail -f $LOG_DIR/subscriber.log"
