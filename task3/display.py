"""
动态曲线显示模块
功能：在终端中实时显示最近 N 个数据点，类似示波器效果
"""

import os
from collections import deque


class CurveDisplay:
	def __init__(self, max_points=20, height=15):
		"""
		初始化曲线显示器

		参数：
			max_points: int - 显示的最大数据点数量
			height: int - 曲线显示的高度（行数）
		"""
		self.max_points = max_points
		self.height = height
		self.data_points = deque(maxlen=max_points)  # 使用双端队列自动维护最近 N 个数据

	def add_data(self, value):
		"""
		添加新数据点

		参数：
			value: int - 新的数据值
		"""
		self.data_points.append(value)

	def display(self):
		"""
		在终端中显示曲线

		TODO: 你的代码
		提示：
		1. 使用 os.system('clear') 或 print('\033[2J\033[H') 清屏
		2. 找出数据的最大值和最小值，用于归一化
		3. 将数据映射到显示高度
		4. 用字符绘制曲线（可以用 * 或 █）
		5. 显示坐标轴和刻度
		"""
		# 清屏
		print('\033[2J\033[H', end='')

		if not self.data_points:
			print("等待数据...")
			return

		# 找出数据范围
		data_list = list(self.data_points)
		min_val = min(data_list)
		max_val = max(data_list)

		# 避免除零
		if max_val == min_val:
			max_val = min_val + 1

		print(f"{'=' * 60}")
		print(f"TCP 数据实时监控 | 最近 {len(data_list)} 个数据点")
		print(f"范围: [{min_val}, {max_val}]")
		print(f"{'=' * 60}\n")

		# 绘制曲线（从上到下）
		for row in range(self.height, -1, -1):
			# 计算当前行对应的数据值
			threshold = min_val + (max_val - min_val) * row / self.height

			# 左侧刻度
			if row == self.height:
				print(f"{max_val:>5} |", end='')
			elif row == 0:
				print(f"{min_val:>5} |", end='')
			elif row == self.height // 2:
				mid_val = (max_val + min_val) // 2
				print(f"{mid_val:>5} |", end='')
			else:
				print("      |", end='')

			# 绘制数据点
			for value in data_list:
				# 判断数据点是否在当前行
				if abs(value - threshold) <= (max_val - min_val) / self.height:
					print(" █", end='')
				else:
					print("  ", end='')

			print()

		# 底部坐标轴
		print("      " + "-" * (self.max_points * 2))
		print(f"      最旧 {'<' * (self.max_points - 5)} 最新\n")


# 测试代码（可选）
if __name__ == '__main__':
	import time
	import random

	display = CurveDisplay(max_points=20, height=15)

	print("动态曲线测试 - 按 Ctrl+C 停止\n")
	time.sleep(2)

	try:
		while True:
			# 生成随机数据
			value = random.randint(0, 100)
			display.add_data(value)
			display.display()
			time.sleep(0.5)
	except KeyboardInterrupt:
		print("\n\n测试结束")
