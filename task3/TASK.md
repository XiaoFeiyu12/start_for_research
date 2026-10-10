# Task 3: Python TCP + MySQL 学习任务

老师的任务：在上一个任务基础上，学习用 Python 操作 MySQL 数据库，将 TCP 服务端接收到的数据保存到数据库，数据库字段包括时间戳、收到的数据、客户端。

## 📁 文件说明

- `README.md` - 详细的学习指南和 API 参考
- `create_table.sql` - MySQL 建表脚本
- `requirements.txt` - Python 依赖包
- `database.py` - 数据库操作类（待实现）
- `client.py` - TCP 客户端（待实现）
- `server.py` - TCP 服务端（待实现）

## 🚀 快速开始

### 1. 安装 Python 依赖

```bash
cd task3
pip install -r requirements.txt
```

### 2. 配置 MySQL 数据库

```bash
# 登录 MySQL（根据你的配置可能需要密码）
mysql -u root -p

# 在 MySQL 中执行建表脚本
source create_table.sql

# 或者直接：
mysql -u root -p < create_table.sql
```

### 3. 实现代码（按顺序）

**Step 1**: 实现 `database.py` 中的方法  
**Step 2**: 实现 `client.py`  
**Step 3**: 实现 `server.py`

每个文件都有详细的 TODO 提示和示例代码！

### 4. 测试

**终端1 - 启动服务端**:
```bash
python server.py 127.0.0.1 8080
```

**终端2 - 启动客户端**:
```bash
python client.py 127.0.0.1 8080
```

**终端3 - 查看数据库**:
```bash
mysql -u root -p tcp_data
# 在 MySQL 中：
SELECT * FROM received_data ORDER BY timestamp DESC LIMIT 10;
```

## 📚 学习重点

### Python Socket 核心概念

**服务端**：`socket()` → `bind()` → `listen()` → `accept()` → `recv()` → `close()`  
**客户端**：`socket()` → `connect()` → `send()` → `close()`

### MySQL 操作核心概念

**连接** → **创建游标** → **执行 SQL** → **提交事务** → **关闭连接**

### 数据打包/解包

- 发送整数：`struct.pack('>i', number)` - 打包成 4 字节
- 接收整数：`struct.unpack('>i', data)[0]` - 解包为整数

## ⚠️ 注意事项

1. **修改数据库密码**：在 `database.py` 和 `server.py` 中修改 `password='your_password'` 为你的 MySQL 密码
2. **字节序**：使用大端字节序 `'>i'`（网络标准）
3. **异常处理**：记得用 `try-except` 捕获异常
4. **资源释放**：在 `finally` 中关闭 socket 和数据库连接

## 🎯 验收标准

- [x] 客户端每秒发送随机数
- [x] 服务端正确接收并打印
- [x] 数据成功存入 MySQL
- [x] 数据库记录包含：时间戳、数据值、客户端地址

## 🐛 调试技巧

- 用 `print()` 在关键步骤打印信息
- 用 MySQL 命令行实时查看数据
- 遇到错误先看异常信息，再检查代码逻辑
- 先测试 `database.py`，再测试网络通讯

祝学习顺利！遇到问题随时问我 😊
