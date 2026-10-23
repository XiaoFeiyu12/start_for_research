import logging
import os

# -----------------------------------------------------------------------
# 提示：用 Python 内置 logging 模块重写 Logger 类
#
# 目标效果：
#   - 同时输出到终端和文件
#   - 终端输出级别可配置（默认 INFO，传 logging.DEBUG 可看到所有）
#   - 文件始终记录所有级别（DEBUG 及以上）
#   - 格式：[时间][名字][级别]:消息
#
# __init__(self, name, log_file=None, console_level=logging.INFO)
#   参数：
#     name          — Logger 名字，用于区分来源，显示在日志里
#     log_file      — 日志文件路径，None 表示只输出终端
#     console_level — 终端显示的最低级别，默认 logging.INFO
#                     传 logging.DEBUG 可看到所有日志
#                     传 logging.WARNING 则终端只显示警告及以上
#
#   步骤：
#   1. self._logger = logging.getLogger(name)
#      self._logger.setLevel(logging.DEBUG)   ← logger 本身设最低，让 handler 各自过滤
#      self._logger.propagate = False         ← 不向上传给 root logger，避免重复输出
#
#   2. 防止重复 addHandler（重复调用 __init__ 会导致同一条日志打印多次）：
#      if self._logger.handlers:
#          return
#
#   3. 创建格式器：
#      logging.Formatter(
#          fmt="[%(asctime)s][%(name)s][%(levelname)s]:%(message)s",
#          datefmt="%Y-%m-%d %H:%M:%S"
#      )
#
#   4. 添加 StreamHandler（终端）：
#      - level 设为 console_level（由调用方决定看哪个级别以上）
#      - 绑定格式器
#      - logger.addHandler(...)
#
#   5. 如果 log_file 不为 None，添加 FileHandler（文件）：
#      - 用 os.path.abspath(log_file) 转绝对路径，避免路径歧义
#      - level 设为 logging.DEBUG（文件记录所有）
#      - 绑定同一个格式器
#      - logger.addHandler(...)
#
# log_info(self, msg)   → self._logger.info(msg)
# log_debug(self, msg)  → self._logger.debug(msg)
# log_warn(self, msg)   → self._logger.warning(msg)
# -----------------------------------------------------------------------


class Logger:
    def __init__(self, name, log_file=None, log_level=logging.INFO):
        self._log_file = log_file

        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)
        self._logger.propagate = False 

        if self._logger.handlers:
            return

        formatter= logging.Formatter(
            fmt="[%(asctime)s][%(name)s][%(levelname)s]:%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S")

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)
        stream_handler.formatter = formatter
        self._logger.addHandler(stream_handler)

        if log_file != None:
            if not os.path.isabs(log_file):
                abs_log_file = os.path.abspath(log_file)
            file_handler = logging.FileHandler(abs_log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.formatter = formatter
            self._logger.addHandler(file_handler) 

    def info(self,msg): self._logger.info(msg)
    def debug(self,msg): self._logger.debug(msg)
    def warning(self,msg): self._logger.warning(msg)
    def error(self,msg): self._logger.error(msg)