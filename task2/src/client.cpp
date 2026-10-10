#include "tools/socket.hpp"
#include <random>
#include <chrono>
#include <thread>

int main(int argc, char** argv)
{
	std::cout << "client starting..." << std::endl;

	// 你的代码：
    std::string ip ;  
    int port ;
    ip = argv[1];
    port = atoi(argv[2]);
	tools::Socket client_socket;
    client_socket.connect(ip, port);

	// 随机数生成器示例
	std::random_device rd;
	std::mt19937 gen(rd());
	std::uniform_int_distribution<> dis(0, 100);

	// 主循环
	while (true)
	{
        int random_num = dis(gen);
		std::cout << "Sending: " << random_num << std::endl;
        client_socket.send_data(&random_num, sizeof(random_num));

        std::this_thread::sleep_for(std::chrono::seconds(1));
	}

	return 0;
}
