# -*- coding: utf-8 -*-
"""
This project has set up a server for communication 
between the front-end and back-end 
Created on Thu Feb  6 16:37:12 2025
@author: Zeyu Pan
version 3
"""
#用于模拟延时
import time

#记录日志


#FAST API 创建 Web API 框架。
from fastapi import HTTPException,FastAPI, UploadFile
from fastapi.responses import JSONResponse

import myLogging
from exception_handler import global_exception_handler  # 导入全局异常处理器

#引入响应和请求
from models import NetworkRequest,NetworkResponse,NoteRequest,NoteResponse,RecordResponse

#引入recordAPI的辅助函数
import recordAPI_helper,noteAPI_helper


#创建了一个 FastAPI 应用实例，用于注册 API 路由和处理请求
app = FastAPI()

# 注册全局异常处理器
app.add_exception_handler(Exception, global_exception_handler)

# 获取默认的日志记录器
logging = myLogging.default_logger

#API 路由

"""
#/test 测试接口
#一个简单的 GET 请求接口，返回字符串。
#会记录日志 Test endpoint accessed.
"""
@app.get("/test")
async def test():
    # logging.info("Test endpoint accessed.")
    return {
        "response": "OK"
    }

"""
#/record 上传录音接口
#模拟处理上传文件的 POST 请求接口。
#返回 RecordResponse，其中包含录音的相关信息（ID、时长、主题等）。
#如果出错，返回 500 错误。
"""
@app.post("/record", response_model=RecordResponse)
async def post_record(file: UploadFile, fake: bool = False):
    """
    #处理上传的音频文件，使用 Whisper 进行语音转文字。
    #:param file: 上传的音频文件
    #:return: 包含转录结果的 JSON 响应
    """
    
    if fake:
       time.sleep(2)  # 模拟延时
       return RecordResponse.fake()
      
    logging.info(f"收到音频文件上传请求: 文件名={file.filename}, 类型={file.content_type}")

    try:
        # 保存上传的文件到临时目录
        saved_file_path = await recordAPI_helper.save_uploaded_file(file)
        logging.info(f"文件保存成功: {saved_file_path}")
        return recordAPI_helper.getResponse(saved_file_path)
    except Exception as e:
        logging.error(f"处理音频文件时发生错误: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

"""
#/note 生成笔记接口
#处理音频转录后的文本，生成笔记，包含主题和摘要。
#该接口接收一个 NoteRequest 请求对象，其中包含音频转录后的文本数据。
#返回 NoteResponse，其中包含生成的笔记信息（主题、摘要等）。
#如果出错，返回 500 错误。
"""
@app.post("/note", response_model=NoteResponse)
async def get_note(note: NoteRequest, fake: bool = False):
    """
    #生成笔记接口
    #接受一个包含音频转录文本的请求，返回生成的笔记（包括主题和摘要）。
    #:param note: 包含音频转录文本的请求对象（NoteRequest），用于生成笔记。
    #:return: 返回包含生成的主题和摘要的笔记响应（NoteResponse）。
    """
    
    if fake:
        time.sleep(2)  # 模拟延时
        return NoteResponse.fake()
    
    try:
        # 获取生成的响应
        note_response = noteAPI_helper.getResponse(note.raw_recognition)
        # 显式返回 JSONResponse，设置 Content-Type 为 utf-8
        return JSONResponse(content=note_response.dict(), headers={"Content-Type": "application/json; charset=utf-8"})
    except Exception as e:
        logging.error(f"生成笔记时发生错误: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")  

"""
#/network 构建知识点网络接口
#处理音频转录后的文本数据，生成与转录内容相关的知识点网络。
#该接口接收一个 NetworkRequest 请求对象，其中包含音频转录后的文本以及其他相关数据。
#返回 NetworkResponse，其中包含生成的知识点网络（如提取的知识点、关系等）。
#如果出错，返回 500 错误。
"""
@app.post("/network", response_model=NetworkResponse)
async def get_network(network: NetworkRequest, fake: bool = False):
    """
    #构建知识点网络接口
    #接受包含音频转录文本和相关请求数据的请求，返回基于转录内容的知识点网络。
    #:param network: 包含音频转录文本和其他相关数据的请求对象（NetworkRequest），用于构建知识点网络。
    #:return: 返回构建的知识点网络响应（NetworkResponse），包含相关的知识点和结构化信息。
    """

    if fake:
        time.sleep(2)  # 模拟延时
        return NetworkResponse.fake()
    
    # try:
    #     #获取响应
    #     return networkAPI_helper.getResponse()
    # except Exception as e:
    #     logging.error(f"构建知识点网络时发生错误: {e}")
    #     raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")