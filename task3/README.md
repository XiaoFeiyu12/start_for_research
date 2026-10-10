# Task 3: Python TCP + MySQL 数据存储

## 学习目标

1. 用 Python 实现 TCP 服务端和客户端
2. 学习使用 MySQL 数据库
3. 将 TCP 接收到的数据存储到数据库

## 项目结构

```
task3/
├── server.py          # TCP 服务端（接收数据并存入数据库）
├── client.py          # TCP 客户端（发送随机数）
├── database.py        # 数据库操作封装类
├── create_table.sql   # 建表 SQL
└── requirements.txt   # Python 依赖
```

## 环境准备

### 1. 安装 MySQL（如果没有）

```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo systemctl start mysql
```

### 2. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 3. 创建数据库和表

```bash
# 登录 MySQL
mysql -u root -p

# 在 MySQL 中执行
source create_table.sql
```

## Python Socket 编程关键 API

### 服务端流程

```python
import socket

# 1. 创建 socket 对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 绑定地址和端口
server_socket.bind((host, port))

# 3. 开始监听
server_socket.listen(backlog)

# 4. 接受客户端连接
client_socket, client_address = server_socket.accept()

# 5. 接收数据
data = client_socket.recv(buffer_size)

# 6. 关闭连接
client_socket.close()
server_socket.close()
```

### 客户端流程

```python
import socket

# 1. 创建 socket 对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 连接服务端
client_socket.connect((host, port))

# 3. 发送数据
client_socket.send(data)

# 4. 关闭连接
client_socket.close()
```

## MySQL 操作关键 API

```python
import mysql.connector

# 1. 连接数据库
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='tcp_data'
)

# 2. 创建游标
cursor = conn.cursor()

# 3. 执行 SQL
cursor.execute("INSERT INTO data_table (...) VALUES (...)", (value1, value2))

# 4. 提交事务
conn.commit()

# 5. 查询数据
cursor.execute("SELECT * FROM data_table")
results = cursor.fetchall()

# 6. 关闭连接
cursor.close()
conn.close()
```

## 学习步骤

### Step 1: 准备数据库（5分钟）
- [ ] 安装 MySQL
- [ ] 运行 `create_table.sql` 建表
- [ ] 用 `mysql` 命令行验证表创建成功

### Step 2: 实现 Database 类（15分钟）
- [ ] 完成 `database.py` 中的 `__init__` 方法（连接数据库）
- [ ] 完成 `insert_data` 方法（插入一条记录）
- [ ] 完成 `get_recent_data` 方法（查询最近N条数据）
- [ ] 测试数据库连接和插入

### Step 3: 实现客户端（10分钟）
- [ ] 完成 `client.py`
- [ ] 每秒生成一个随机数并发送
- [ ] 打印发送的数据

### Step 4: 实现服务端（20分钟）
- [ ] 完成 `server.py` 中的 socket 监听部分
- [ ] 接收客户端数据
- [ ] 调用 Database 类存入数据库
- [ ] 打印接收到的数据

### Step 5: 联调测试（10分钟）
- [ ] 启动服务端
- [ ] 启动客户端
- [ ] 用 MySQL 查看数据是否正确存入

## 注意事项

1. **字节序问题**：Python 发送整数时需要用 `struct.pack()` 打包，接收时用 `struct.unpack()` 解包
2. **数据库连接**：记得修改 `database.py` 中的用户名和密码
3. **异常处理**：网络和数据库操作都需要 try-except
4. **资源释放**：记得关闭 socket 和数据库连接

## 调试技巧

- 服务端和客户端分别在两个终端运行
- 用 `print()` 打印关键步骤
- 用 `mysql` 命令行实时查看数据：
  ```sql
  SELECT * FROM tcp_data ORDER BY timestamp DESC LIMIT 10;
  ```
