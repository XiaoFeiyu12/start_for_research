# Python logging 模块学习笔记

## 1. 为什么用 logging 而不是 print

`print()` 没有级别区分、不能过滤、重定向到文件后终端看不到。
`logging` 解决了这些问题，是生产代码的标准做法。

---

## 2. 日志级别

从低到高：

| 级别 | 数值 | 用途 |
|------|------|------|
| DEBUG | 10 | 调试信息，细节 |
| INFO | 20 | 正常运行信息 |
| WARNING | 30 | 警告，程序还能运行 |
| ERROR | 40 | 错误，某个功能失败 |
| CRITICAL | 50 | 严重错误，程序可能崩溃 |

设置 `level=logging.INFO`，则 DEBUG 消息会被过滤掉，INFO 及以上的才会输出。
每个 Handler 可以单独设置 level，实现"终端只看 INFO，文件记录所有 DEBUG"。

---

## 3. 三个核心对象

### Logger — 日志记录器
你拿来写日志的对象，通过名字区分来源：

```python
import logging
logger = logging.getLogger("MqttSubscriber")
logger.setLevel(logging.DEBUG)  # 设置最低记录级别

logger.debug("调试信息")
logger.info("正常信息")
logger.warning("警告")
logger.error("错误")
```

`getLogger(name)` 同名多次调用返回同一个对象（单例），不会重复创建。

### Handler — 处理器
决定日志往哪里输出，一个 Logger 可以挂多个 Handler：

```python
# 输出到终端
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)   # 终端只显示 INFO 以上

# 输出到文件
file_handler = logging.FileHandler("app.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)    # 文件记录所有级别

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
```

### Formatter — 格式器
控制每条日志长什么样：

```python
fmt = logging.Formatter(
    fmt="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
stream_handler.setFormatter(fmt)
file_handler.setFormatter(fmt)
```

常用的格式字段：

| 字段 | 含义 |
|------|------|
| `%(asctime)s` | 时间，格式由 `datefmt` 控制 |
| `%(name)s` | Logger 的名字 |
| `%(levelname)s` | 级别名称（INFO、DEBUG 等） |
| `%(message)s` | 日志内容 |
| `%(filename)s` | 源文件名 |
| `%(lineno)d` | 行号 |

---

## 4. 完整示例

```python
import logging

def create_logger(name, log_file):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "[%(asctime)s][%(name)s][%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 终端 Handler
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(fmt)

    # 文件 Handler
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    logger.addHandler(sh)
    logger.addHandler(fh)
    return logger

logger = create_logger("MyApp", "app.log")
logger.debug("这条只写文件，终端看不到")
logger.info("这条终端和文件都有")
logger.warning("警告！")
```

---

## 5. 注意事项

**重复 Handler 问题**
`getLogger(name)` 返回同一个对象，如果多次调用 `addHandler()`，同一条日志会被输出多次。
避免方法：创建前检查 `if not logger.handlers:`，或者只在程序入口初始化一次。

**propagate**
Logger 默认会把日志传递给父级 Logger（最顶层是 root logger）。
如果 root logger 也有 Handler，可能造成重复输出。
可以设置 `logger.propagate = False` 关闭向上传递。

**FileHandler 的 mode 参数**
默认 `mode='a'`（追加），每次运行都追加到同一文件。
如果想每次运行都清空重写，用 `mode='w'`。

**日志文件路径**
`FileHandler` 的路径是相对于**当前工作目录**的，不是脚本所在目录。
建议传绝对路径，或者在调用方计算好路径再传进来。
