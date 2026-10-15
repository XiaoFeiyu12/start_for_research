# RESTful API 与 Flask 学习笔记

## 1. HTTP 基础

Web 服务建立在 HTTP 协议上。HTTP 也是基于 TCP 的，和 task3 的 TCP 通信本质一样，区别是 HTTP 规定了消息的格式。

**请求（Request）** — 客户端发给服务器：
```
GET /api/data?start=2026-10-01&end=2026-10-10 HTTP/1.1
Host: localhost:8000
```

**响应（Response）** — 服务器返回给客户端：
```
HTTP/1.1 200 OK
Content-Type: application/json

{"code": 0, "count": 2, "data": [...]}
```

Flask 帮你处理了所有 HTTP 格式解析，你只需要：
- 取参数：`request.args.get("start")`
- 返回数据：`return jsonify({...}), 200`

---

## 2. 什么是 RESTful API

REST（Representational State Transfer）是一种 Web API 设计风格，核心思想是：
**用 URL 表示资源，用 HTTP 方法表示操作**。

| HTTP 方法 | 含义 | 例子 |
|-----------|------|------|
| GET | 查询 | `GET /api/data` 查询数据 |
| POST | 创建 | `POST /api/data` 新增数据 |
| PUT | 整体更新 | `PUT /api/data/1` 更新ID=1的记录 |
| DELETE | 删除 | `DELETE /api/data/1` 删除ID=1 |

本任务只用 GET，实现查询。

---

## 2. URL 参数的两种方式

**路径参数**（资源的唯一标识）：
```
GET /api/data/42        ← 查 ID=42 的记录
```

**查询参数**（过滤/搜索条件，`?key=value` 格式）：
```
GET /api/data?start=2026-10-01&end=2026-10-10
```

时间段查询用查询参数更合适，Flask 里用 `request.args.get("start")` 取。

---

## 3. Flask 基础用法

Flask 是 Python 最流行的轻量 Web 框架，用装饰器把函数绑定到 URL。

### 安装
```bash
pip3 install flask
```

### 最简单的例子
```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/api/hello", methods=["GET"])
def hello():
    return jsonify({"message": "hello world"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
```

### 路由装饰器
```python
@app.route("/api/data", methods=["GET"])      # 只接受 GET
@app.route("/api/data/<int:id>", methods=["GET"])  # 路径参数，自动转 int
```

### 取查询参数
```python
@app.route("/api/data", methods=["GET"])
def get_data():
    start = request.args.get("start")   # ?start=xxx，没传返回 None
    end   = request.args.get("end", default="2099-01-01")  # 带默认值
```

### 返回 JSON 响应
```python
# 成功
return jsonify({"code": 0, "data": [...]}), 200

# 参数错误
return jsonify({"code": 400, "message": "缺少参数 start"}), 400

# 服务器内部错误
return jsonify({"code": 500, "message": str(e)}), 500
```

`jsonify()` 把 Python dict/list 转成 JSON 响应，自动设置 Content-Type。

---

## 4. HTTP 状态码

| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数有误（客户端的锅） |
| 404 | 资源不存在 |
| 500 | 服务器内部错误（服务端的锅） |

---

## 5. 本任务 API 设计

```
GET /api/data?start=<时间>&end=<时间>
```

请求示例：
```
GET http://localhost:8000/api/data?start=2026-10-01 00:00:00&end=2026-10-10 23:59:59
```

响应示例：
```json
{
  "code": 0,
  "count": 3,
  "data": [
    {"id": 1, "timestamp": "2026-10-01 10:00:01", "value": 42, "client": "127.0.0.1:8080"},
    {"id": 2, "timestamp": "2026-10-01 10:00:02", "value": 17, "client": "127.0.0.1:8080"}
  ]
}
```

---

## 6. 用 curl 测试 API

```bash
# 基本查询
curl "http://localhost:8000/api/data?start=2026-10-01 00:00:00&end=2026-10-10 23:59:59"

# 格式化输出（需要安装 jq）
curl -s "http://localhost:8000/api/data?start=2026-10-01&end=2026-10-10" | jq .

# 也可以直接在浏览器访问
```

---

## 7. CORS 跨域（了解）

如果前端页面和 API 不在同一个端口，浏览器会因为跨域策略拒绝请求。
Flask 用 `flask-cors` 解决：

```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # 允许所有来源跨域
```

本任务不涉及前端，暂时不需要处理。
