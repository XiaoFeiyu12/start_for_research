-- ==============================================================
-- Task 3: SQL 学习 - 创建数据库和表
-- ==============================================================
--
-- 学习目标：
-- 1. 理解如何创建数据库
-- 2. 理解如何创建数据表
-- 3. 掌握常用的字段类型（INT, DATETIME, VARCHAR）
-- 4. 学习基本的 SQL 查询语句
--
-- 提示：
-- - 以 -- 开头的是注释
-- - SQL 语句以分号 ; 结尾
-- - SQL 关键字建议大写（CREATE, SELECT 等）
-- - 删除 TODO 注释后写你的代码
-- ==============================================================

-- TODO 1: 创建数据库
-- 提示：
-- CREATE DATABASE IF NOT EXISTS 数据库名称;
-- 数据库名称：tcp_data

-- 你的代码：
CREATE DATABASE IF NOT EXISTS tcp_data;



-- TODO 2: 切换到这个数据库
-- 提示：
-- USE 数据库名称;

-- 你的代码：
USE tcp_data;


-- TODO 3: 创建数据表
-- 提示：
-- CREATE TABLE IF NOT EXISTS 表名 (
--     字段1 类型 约束,
--     字段2 类型 约束,
--     ...
-- );
--
-- 表名：received_data
--
-- 字段要求：
-- 1. id - 整数类型，自增，主键
--    INT AUTO_INCREMENT PRIMARY KEY
--
-- 2. timestamp - 日期时间类型，不能为空，默认值为当前时间
--    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
--
-- 3. data_value - 整数类型，不能为空，用于存储接收到的数据
--    INT NOT NULL
--
-- 4. client_address - 字符串类型，最大长度50，不能为空，存储客户端地址
--    VARCHAR(50) NOT NULL

-- 你的代码：
CREATE TABLE IF NOT EXISTS received_data(
id INT AUTO_INCREMENT PRIMARY KEY,
timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
data_value INT NOT NULL,
client_address VARCHAR(50) NOT NULL
);


-- ==============================================================
-- 下面是一些常用的 SQL 查询命令（供测试用）
-- 去掉前面的 -- 就可以执行
-- ==============================================================

-- 查看表结构
-- DESC received_data;

-- 测试插入一条数据
-- INSERT INTO received_data (data_value, client_address) VALUES (42, '127.0.0.1:12345');

-- 查询所有数据
-- SELECT * FROM received_data;

-- 查询最近10条数据（按时间倒序）
-- SELECT * FROM received_data ORDER BY timestamp DESC LIMIT 10;

-- 查询特定客户端的数据
-- SELECT * FROM received_data WHERE client_address = '127.0.0.1:12345';

-- 统计总记录数
-- SELECT COUNT(*) FROM received_data;

-- 计算数据的平均值
-- SELECT AVG(data_value) FROM received_data;

-- 删除所有数据（危险操作！）
-- DELETE FROM received_data;
