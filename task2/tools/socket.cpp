#include "socket.hpp"

namespace tools
{

Socket::Socket() : ip_(""), port_(0), socketfd_(0)
{
	socketfd_ = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	if (socketfd_ < 0)
	{
		std::cerr << "failed to create socket, errno=" << errno << std::endl;
	}
}

Socket::~Socket()
{
	close(socketfd_);
}

bool Socket::bind(const std::string &ip, int port)
{

	ip_ = ip;
	port_ = port;

    sockaddr_in sockaddr;
    std::memset(&sockaddr, 0, sizeof(sockaddr));
    sockaddr.sin_family = AF_INET;
    sockaddr.sin_port = htons(port_);
    inet_pton(AF_INET, ip.c_str(), &sockaddr.sin_addr);
    if(::bind(socketfd_, (struct sockaddr *)&sockaddr, sizeof(sockaddr)) < 0)
    {
        std::cerr << "fail to bind, errno=" << errno << std::endl;
        return false;
    }
    else
    {
        return true;
    }
	
}

bool Socket::listen(int backlog)
{
    if(::listen(socketfd_, backlog) <0)
    {
        std::cerr << "fail to listen, errno=" << errno << std::endl;
        return false;
    }
    else
    {
        return true;
    }
	
}

int Socket::accept()
{
    sockaddr_in client_addr;
    socklen_t addr_len = sizeof(client_addr);
    int fd = ::accept(socketfd_,(struct sockaddr*)&client_addr,&addr_len);
    if(fd < 0)
    {
        std::cerr << "fail to accept, errno=" << errno << std::endl;
        return -1;
    }
    else
    {
		char client_ip[INET_ADDRSTRLEN];
		inet_ntop(AF_INET, &client_addr.sin_addr, client_ip, INET_ADDRSTRLEN);
        std::cout << "client IP:" << client_ip << " port:" << ntohs(client_addr.sin_port) << std::endl;
        return fd;
    }
	
}

bool Socket::connect(const std::string &ip, int port)
{
	ip_ = ip;
	port_ = port;

    sockaddr_in sockaddr;
    std::memset(&sockaddr, 0, sizeof(sockaddr));
    sockaddr.sin_family = AF_INET;
    sockaddr.sin_port = htons(port_);
    inet_pton(AF_INET, ip.c_str(), &sockaddr.sin_addr);
    if(::connect(socketfd_, (struct sockaddr *)&sockaddr, sizeof(sockaddr)) < 0)
    {
        std::cerr << "fail to connect, errno=" << errno << std::endl;
        return false;
    }
    else
    {
        return true;
    }
}

int Socket::send_data(const void *data, size_t size)
{
    int num = ::send(socketfd_, data, size, 0);

    if (num == -1)
    {
        std::cerr << "fail to send data, errno=" << errno << std::endl;
    }


	return num;
}

int Socket::recv_data(void *buffer, size_t size)
{
    int num = ::recv(socketfd_, buffer, size, 0);

    if (num == -1)
    {
        std::cerr << "fail to recv data, errno=" << errno << std::endl;
    }
    else if (num == 0)
    {
        std::cout << "the connection has closed" << std::endl;
    }


	return num;
}

}  // namespace tools