#ifndef __SOCKET_HPP
#define __SOCKET_HPP

#include <iostream>
#include <string>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <cstring>
#include <errno.h>

namespace tools
{

class Socket
{
public:
	Socket();
	~Socket();

	// 服务端方法
	bool bind(const std::string &ip, int port);
	bool listen(int backlog = 5);
	int accept();  // 返回新连接的 socket fd，失败返回 -1

	// 客户端方法
	bool connect(const std::string &ip, int port);

	// 通用收发方法
	int send_data(const void *data, size_t size);  // 返回实际发送字节数
	int recv_data(void *buffer, size_t size);      // 返回实际接收字节数

	int get_socketfd() const { return socketfd_; }

protected:
	std::string ip_;
	int port_;
	int socketfd_;
};

}

#endif