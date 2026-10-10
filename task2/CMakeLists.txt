cmake_minimum_required(VERSION 3.16)

project(tcp_demo)
set(CMAKE_CXX_STANDARD 17)

# Qt 相关设置
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)
find_package(Qt5 COMPONENTS Core Widgets Charts REQUIRED)

add_subdirectory(tools)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

# 客户端（终端版本）
add_executable(client src/client.cpp)
target_link_libraries(client tools)

# 服务端（Qt GUI 版本）
add_executable(server src/server.cpp)
target_link_libraries(server
	tools
	Qt5::Core
	Qt5::Widgets
	Qt5::Charts
)
