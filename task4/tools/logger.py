from datetime import datetime


class Logger:
    def __init__(self,name):
        self.name = name

    def log_info(self,msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        print(f"[{timestamp}][{self.name}][INFO]:{msg}")

    def log_debug(self,msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        print(f"[{timestamp}][{self.name}][DEBUG]:{msg}")

    def log_warn(self,msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        print(f"[{timestamp}][{self.name}][WARN]:{msg}")