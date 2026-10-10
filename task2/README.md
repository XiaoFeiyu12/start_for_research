# TCP 通讯学习指南

## 项目结构
```
task2/
├── tools/
│   ├── socket.hpp       # Socket 类声明
│   └── socket.cpp       # Socket 类实现（需要你补充）
├── src/
│   ├── server.cpp       # 服务端程序（需要你补充）
│   └── client.cpp       # 客户端程序（需要你补充）
└── CMakeLists.txt
```

## 编译和运行
```bash
cd /home/xiaofeiyu/research_ws/start_for_research/task2
mkdir build && cd build
cmake ..
make

# 先启动服务端
./server

# 再启动客户端（另一个终端）
./client
```

## 学习步骤建议

### 第一步：实现 Socket 类的基础方法
按顺序实现 `socket.cpp` 中的函数：
1. `~Socket()` - 最简单，只需 close
2. `bind()` - 服务端绑定地址
3. `listen()` - 服务端开始监听
4. `accept()` - 服务端接受连接
5. `connect()` - 客户端连接服务端
6. `send_data()` - 发送数据
7. `recv_data()` - 接收数据

### 第二步：实现简单的客户端
在 `client.cpp` 中：
1. 连接到服务端
2. 每秒生成一个随机数并发送
3. 打印发送的数据

### 第三步：实现简单的服务端
在 `server.cpp` 中：
1. 绑定地址并监听
2. 接受客户端连接
3. 循环接收数据并打印

### 第四步：实现动态曲线显示
在 `server.cpp` 中实现 `display_curve()` 函数：
1. 维护最近 20 个数据点
2. 用字符绘制动态曲线

## 关键 API 速查

### socket() - 创建套接字
```cpp
int sockfd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
```

### bind() - 绑定地址（服务端）
```cpp
struct sockaddr_in addr;
addr.sin_family = AF_INET;
addr.sin_port = htons(port);               // 主机序转网络序
inet_pton(AF_INET, ip.c_str(), &addr.sin_addr);  // 或用 inet_addr()
::bind(sockfd, (struct sockaddr*)&addr, sizeof(addr));
```

### listen() - 监听（服务端）
```cpp
::listen(sockfd, backlog);
```

### accept() - 接受连接（服务端）
```cpp
struct sockaddr_in client_addr;
socklen_t addr_len = sizeof(client_addr);
int client_fd = ::accept(sockfd, (struct sockaddr*)&client_addr, &addr_len);
```

### connect() - 连接（客户端）
```cpp
struct sockaddr_in addr;
// 设置 addr（同 bind）
::connect(sockfd, (struct sockaddr*)&addr, sizeof(addr));
```

### send() / recv() - 收发数据
```cpp
::send(sockfd, data, size, 0);
::recv(sockfd, buffer, size, 0);
```

### close() - 关闭套接字
```cpp
close(sockfd);
```

## 注意事项

1. **字节序**：网络传输使用大端序（网络序），主机可能是小端序
   - 端口号：`htons()` / `ntohs()`
   - IP地址：`htonl()` / `ntohl()`
   - 发送数据时也要注意字节序

2. **错误处理**：每个系统调用都应该检查返回值
   - 失败时返回 -1，可以用 `errno` 或 `strerror(errno)` 查看错误

3. **阻塞 vs 非阻塞**：
   - `accept()` 和 `recv()` 默认是阻塞的
   - 本任务中使用阻塞模式即可

4. **数据完整性**：
   - `send()` 可能不会一次发送完所有数据
   - `recv()` 可能收到部分数据
   - 本任务中传输 int 比较小，通常不会有问题

## 动态显示的实现思路

### 方法 1：横向滚动（推荐）
```
最近 20 个数据横向显示：
100 |                    *
 75 |          *    *   
 50 |    *                *
 25 | *      *        *
  0 |___________________
```

### 方法 2：纵向滚动
```
新数据不断向上滚动，类似终端输出
```

提示：
- 用 `\033[2J\033[H` 清屏
- 或用 `\r` 加固定行数的输出覆盖显示
- 计算数据到字符高度的映射关系

## 参考资源

- `man 2 socket` - 查看系统调用手册
- `man 7 ip` - 查看 IP 协议相关
- Beej's Guide to Network Programming（经典网络编程教程）

## 调试技巧

1. 先让程序跑起来，能连接、能收发
2. 再优化显示效果
3. 用 `std::cout` 打印中间状态
4. 检查返回值，出错时打印 `errno` 和 `strerror(errno)`

祝学习顺利！遇到具体问题随时问我。
