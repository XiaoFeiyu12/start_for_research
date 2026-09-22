import csv
from datetime import datetime
from pathlib import Path

def format_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d, %H:%M:%S")

if __name__ == '__main__':
    # 获取文件夹路径
    folder_input = input("请输入目标文件夹:").strip()
    folder = Path(folder_input)

    #打开文件夹
    if not folder.exists():
        print("文件夹不存在")
    if folder.is_file():
        print("路径为文件")
    else:
        # 创建CSV文件
        output_file = folder/"文件信息.csv"
        # 获取文件句柄
        with open (output_file,"w",newline="",encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["文件名","文件路径","文件大小/字节","创建时间"])
        # 读取文件夹下所有文件
            for item in folder.rglob("*"):
                if item.is_file() and item!=output_file:
                    #获取文件信息
                    file_info = item.stat()

                    csv_writer.writerow([
                        item.name,
                        str(item),
                        file_info.st_size,
                        format_time(file_info.st_birthtime)
                    ])

                    print(f"文件名{item.name}",
                          f"文件路径{str(item)}",
                          f"文件大小/字节{file_info.st_size}",
                          f"创建时间{format_time(file_info.st_birthtime)}")

            print(f"信息已保存至{output_file}")
