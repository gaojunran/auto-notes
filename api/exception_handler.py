# -*- coding: utf-8 -*-
"""
This file used to handle exceptions.
Created on Sun Jan 26 16:49:19 2025
@author: Zeyu Pan
version 2
"""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import myLogging
import traceback

# 获取默认的日志记录器
logger = myLogging.default_logger

# 全局异常处理器
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        # 针对 HTTPException 返回相应的 status_code 和 detail
        logger.error(f"HTTPException: {exc.detail}, traceback: {traceback.format_exc()}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail}  # 使用异常中提供的 detail 信息
        )
    else:
        # 其他未知异常
        logger.error(f"Unhandled exception: {exc}, traceback: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"message": "服务器内部错误，请稍后重试"}
        )
