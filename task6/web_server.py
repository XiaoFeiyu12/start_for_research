"""
Flask RESTful API 服务
功能：提供查询 MySQL 时间段数据的 HTTP 接口

API：GET /api/data?start=<时间>&end=<时间>
"""

# 需要导入的库：sys, flask(Flask, jsonify, request), database, tools.logger
import sys
from flask import Flask, jsonify, request, send_from_directory
from database import Database, DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
from tools.logger import Logger

# -----------------------------------------------------------------------
# 提示：整体结构
#
# 1. 初始化 Flask app 和 Logger：
#    app = Flask(__name__)
#    logger = Logger("WebServer", log_file="logs/web_server.log")
#
# 2. 初始化数据库连接（全局，供路由函数使用）：
#    db = Database(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
#
# 3. 定义路由 GET /api/data：
#
#    @app.route("/api/data", methods=["GET"])
#    def get_data():
#      - 用 request.args.get("start") 和 request.args.get("end") 获取参数
#      - 如果 start 或 end 为 None，返回 400：
#        return jsonify({"code": 400, "message": "缺少参数 start 或 end"}), 400
#      - 调用 db.get_data_by_time_range(start, end) 查询
#      - 把结果（元组列表）转换为 dict 列表，方便 JSON 序列化：
#        [{"id": r[0], "timestamp": str(r[1]), "value": r[2], "client": r[3]} for r in rows]
#      - 返回 200：
#        return jsonify({"code": 0, "count": len(data), "data": data}), 200
#      - 用 try/except Exception 包裹，出错返回 500
#
# 4. main() 里启动服务：
#    app.run(host="0.0.0.0", port=8000, debug=False)
#    （debug=True 会开启热重载，但多线程时可能有问题，生产环境关掉）
# -----------------------------------------------------------------------

logger = Logger("WebServer", "logs/web_server.log")
app = Flask(__name__)
db = Database(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/api/data", methods=["GET"])
def get_data():
    try:
        start = request.args.get("start")
        end = request.args.get("end")

        if start == None or end == None:
            logger.error("返回码:400 缺少参数start或者end")
            return jsonify([{"code": 400, "message": "缺少参数start或者end"}]), 400

        datas = db.get_data_by_time_range(start, end)
        result = []
        for data in datas:
            result.append(
                {
                    "id": data[0],
                    "timestamp": str(data[1]),
                    "value": data[2],
                    "client": data[3],
                }
            )
            logger.debug(
                f"返回数据:('id': {data[0]}, 'timestamp': {str(data[1])}, 'value': {data[2]}, 'client': {data[3]})"
            )
        return jsonify([{"code": 0, "count": len(result), "data": result}]), 200
    except Exception as e:
        logger.error(f"网页服务端出错:{e}")
        return jsonify({"code": 500, "message": f"网页服务端出错:{e}"})


def main():
    app.run(host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
