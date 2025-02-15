# -*- coding: utf-8 -*-
"""
This file is used to record logs
Created on Fri Feb  7 19:10:20 2025
@author: Zeyu Pan
version 3
"""
import logging
import os

# 初始化日志配置的函数
def setup_logger(name, log_file, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        # 创建文件处理器
        try:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
        except Exception as e:
            print(f"无法创建日志文件 {log_file}: {e}")
            file_handler = None

        # 创建控制台处理器
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)

        # 日志格式
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        
        if file_handler:
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger

# 选择日志路径
DEBUG_MODE=True
#DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

if DEBUG_MODE:
    #print("调试模式")
    log_path = "api.log"  # 调试时日志文件
else:
    #print("生产模式")
    if os.name == 'nt':  # Windows
        home_dir = os.getenv("USERPROFILE")
        log_dir = os.path.join(home_dir, "AppData", "Local", "com.auto-notes.app", "logs")
    elif os.name == 'posix':  # macOS/Linux
        home_dir = os.getenv("HOME")
        log_dir = os.path.join(home_dir, "Library", "Logs", "com.auto-notes.app")
    else:
        raise EnvironmentError("Unsupported OS")

    # 确保日志目录存在
    try:
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "api.log")
    except PermissionError:
        log_path = "api.log"  # 退回到本地日志路径
        print(f"⚠️ 无法创建日志目录: {log_dir}, 使用本地日志文件 {log_path}")

# 创建默认日志记录器
default_logger = setup_logger('default_logger', log_path)
