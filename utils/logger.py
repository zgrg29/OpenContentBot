import logging
import sys
from logging.handlers import RotatingFileHandler
import os

# 确保日志目录存在
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 创建日志记录器
logger = logging.getLogger("OpenContentBot")
logger.setLevel(logging.INFO)

# 定义日志格式
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 1. 控制台输出
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 2. 文件输出 (保留最近 5 个文件，每个最大 5MB)
file_handler = RotatingFileHandler(
    os.path.join(log_dir, "bot.log"), 
    maxBytes=5*1024*1024, 
    backupCount=5,
    encoding='utf-8'
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)