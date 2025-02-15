# -*- coding: utf-8 -*-
"""
This file provides help methods for the record API
Created on Thu Feb  6 21:40:30 2025
@author: Zeyu Pan
version 2
"""
#这里用它来判断输入的文件是否为视频文件。
import mimetypes

#用来调用 ffmpeg 工具，将视频文件转换为音频文件。
import subprocess

#记录日志
import myLogging

#用来判断是否有可用的 GPU，并且加载 Whisper 模型时，会将模型加载到 GPU 上（如果可用）以提高处理速度。
import torch

from openai import OpenAI
import whisper
import tempfile
import os
import warnings
from entities import RawRecognition
import time

#引入响应和请求
import models

# 获取默认的日志记录器
logging = myLogging.default_logger

"""
判断文件是否为视频格式
"""
def is_video_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith("video")

"""
检查用户是否有ffmpeg 如果没有，安装ffmpeg
"""
def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        logging.info("ffmpeg 已安装")
    except subprocess.CalledProcessError:
        logging.warning("ffmpeg 未安装，开始安装...")
        if os.name == 'nt':  # Windows 系统
            install_ffmpeg_windows()
        elif os.name == 'posix':  # macOS 或 Linux 系统
            install_ffmpeg_mac()
        else:
            logging.error("不支持的操作系统")
            raise RuntimeError("不支持的操作系统，无法安装 ffmpeg")

"""
Windows安装ffmpeg
"""
def install_ffmpeg_windows():
    try:
        subprocess.run(['choco', 'install', 'ffmpeg', '-y'], check=True)
        logging.info("ffmpeg 安装完成")
    except subprocess.CalledProcessError:
        logging.error("Chocolatey 安装失败，尝试手动安装 ffmpeg")
        raise RuntimeError("Windows 系统下 ffmpeg 安装失败")

"""
Mac安装ffmpeg
"""
def install_ffmpeg_mac():
    try:
        subprocess.run(['brew', 'install', 'ffmpeg'], check=True)
        logging.info("ffmpeg 安装完成")
    except subprocess.CalledProcessError:
        logging.error("Homebrew 安装失败，尝试手动安装 ffmpeg")
        raise RuntimeError("macOS 系统下 ffmpeg 安装失败")

"""
将视频文件转换为音频文件。若输入文件是视频格式，则使用 ffmpeg 转换。
:param file_path: 输入的视频文件路径
:param audio_file_path: 生成的音频文件路径（默认输出格式为wav）
"""
def video_to_audio(file_path: str, audio_file_path:str):
    
    # 检查并转换视频文件为音频文件
    try:
        if is_video_file(file_path):
            # 检查用户是否有ffmpeg 如果没有，安装ffmpeg
            check_ffmpeg()
            # 使用 ffmpeg 提取视频中的音频
            command = f"ffmpeg -y -i {file_path} -vn -acodec copy {audio_file_path}"
            # 执行转换命令
            subprocess.run(command, shell=True)
            logging.info(f"视频文件 {file_path} 转换为音频成功: {audio_file_path}")
            return audio_file_path
        else:
            return file_path
            
    except subprocess.CalledProcessError as e:
        logging.error(f"转换过程中出现错误: {e}")
        raise RuntimeError(f"转换失败：{e}")
        
"""
# 保存上传的文件到临时目录
"""
async def save_uploaded_file(file):
    filename = file.filename.lower()
    suffix = os.path.splitext(filename)[1].lower()
    
    try:
        if is_video_file(file.filename):
            logging.info("收到视频文件 正在处理")
            # 如果是视频文件，首先保存它并转换为音频
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(await file.read())
                temp_file_path = temp_file.name

            # 视频转音频
            audio_file_path = temp_file_path.replace(suffix, ".m4a")
            video_to_audio(temp_file_path, audio_file_path)
            return audio_file_path  # 返回转换后的音频文件路径
        elif is_audio_file(file.filename):
            # 如果是音频文件，直接保存它
            logging.info("收到音频文件 正在处理")
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(await file.read())
                temp_file_path = temp_file.name
                #logging.info(f"音频文件已保存到临时文件: {temp_file_path}")
            return temp_file_path
        else:
            raise ValueError("Uploaded file is not supported.")

    except Exception as e:
        logging.error(f"保存文件时发生错误: {e}")
        raise e

"""
# 判断文件是否为音频格式
"""
def is_audio_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith("audio")

"""
#检查当前是否有 GPU 可用
"""
def check_gpu():
        if torch.cuda.is_available():
            logging.info(f"GPU is available: {torch.cuda.get_device_name(0)}")
        else:
            logging.info("GPU is not available.")
            
"""
#返回设备类型，若有 GPU 可用则返回 'cuda'，否则返回 'cpu'
"""
def check_device():
        return "cuda" if torch.cuda.is_available() else "cpu"

"""
# 加载 Whisper 模型
"""
def load_whisper(device:str):
    #设定要下载的模型类型
    if device=="cuda":
        model_type="turbo"
        #model_type="base"
    else:
        model_type="base"
        
    try:
        logging.info("加载 Whisper 模型中...")
        # 可选择 'tiny', 'base', 'small', 'medium', 'large' (for cpu) 'turbo' for gpu
        model = whisper.load_model(model_type).to(device)  
        logging.info(f"Whisper 模型加载成功！模型为：{model_type}")
        return model
    except Exception as e:
        logging.critical(f"Whisper 模型加载失败: {e}")
        raise RuntimeError("模型加载失败，请检查配置。")
        
"""    
#上传文件并转文字 控制台交互不需要最后一个输出文件的参数 注意修改
"""
def transcribe_audio(file_path: str, model,output_file: str,device:str):
    try:
        logging.info(f"正在处理音频文件: {file_path}")
        
        # 根据设备类型选择是否启用 fp16 (半精度浮点数)
        if device == "cuda":
            logging.info("GPU 可用，使用 fp16 精度")
            result = model.transcribe(file_path, fp16=True)
        else:
            logging.info("使用 CPU，禁用 fp16")
            result = model.transcribe(file_path, fp16=False) 
        logging.info("语音转文字完成！")
        
        #检查转录结果是否为空
        if result["text"] is None:
            raise ValueError("转录结果为空.")

        # 提取时间戳和文本段落
        segments = result['segments']  # 包含每段的时间戳和文本
        
        # 将结果写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            time_text_list=[]
            for segment in segments:
                start_time = segment["start"]
                #将时间格式转换为hh：mm：ss的格式
                formatted_time = (
                    f"{int(start_time // 3600):02}:{int((start_time % 3600) // 60):02}:{int(start_time % 60):02}"
                )
                text = segment["text"]
                line=formatted_time+"\t"+ text+"\n"
                time_text_list.append(line)
                f.write(line)
                
            return time_text_list
        
    except Exception as e:
        logging.error(f"语音转文字失败: {e}")
        raise RuntimeError("转文字失败，请重试")

"""
#生成主题和摘要
"""
def get_topic_and_abstract(text):
    # 如果输入文本为空或仅包含空白字符，则抛出异常
    if text is None or text.strip() == "":
        raise ValueError("No text provided for topic and abstract generation.")

    # 初始化 OpenAI 客户端（在这里使用的是 Zhipu AI）
    client = OpenAI(
         # Zhipu AI API key
         api_key="0f78283e98d641af831083f72612950b.ZyRMh52V3a4LmmRy",
         base_url="https://open.bigmodel.cn/api/paas/v4",  # Ensure URL is correct
    )

    # 构建生成主题和摘要的提示语（prompt），通过这个提示来引导 AI 生成我们想要的结果
    prompt = (
        f"请根据以下内容生成一个简洁的主题和摘要（请用Markdown格式）:\n\n{text}\n\n"
        "主题应是对内容的核心主题进行简洁的总结，摘要应对内容进行简要概括,一句话即可。"
        "注意，主题应该只有一个中心词，像‘排列’，‘矩阵’这样的回复就很好，不要在中心词后面加‘定义’、‘应用’、‘简介’等，像‘讲解排列及其相关概念’这样的回复就不够好，我希望的回复是‘排列’"
        "主题和摘要中要避免明显的错误，比如‘鸡排列’当更正为‘奇排列’，这些最基本的术语我相信你是可以识别出来的"
        "回复中直接给我结果，不用'主题:'和'摘要:'这样格式的提示词"
        "请用与输入的文本一样的语言回复，英文文本就用英文回复，中文文本就用中文回复"
    )

    try:
        # 向 AI 模型发送请求并获取回复，指定使用的模型（glm-4）
        completion = client.chat.completions.create(
            model="glm-4",  # Make sure this is the correct model name
            messages=[
                {"role": "user", "content": prompt},
            ],
        )

        # 获取 AI 返回的内容，这里是主题和摘要的文本
        result = completion.choices[0].message.content.strip()

        # 通过换行符将返回的内容分割成主题和摘要
        topic, abstract = result.split('\n', 1)  # 假设 AI 返回的内容第一行是主题，后面的部分是摘要

        return {"topic": topic.strip(), "abstract": abstract.strip()}
    
    except Exception as e:
        raise RuntimeError(f"Error generating topic and abstract: {str(e)}")
    
#将 hh：mm：ss格式的时间换算成秒
def time_conversion(formatted_time:str):
    # 将字符串按 ':' 分割为小时、分钟、秒
    hours, minutes, seconds = map(int, formatted_time.split(':'))
    # 将时间转换为秒
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

"""
生成响应
"""
def getResponse(file):

    # 设置音频文件路径
    audio_file = file

    # 获取文件所在目录
    file_dir = os.path.dirname(audio_file)

    # 在相同目录下创建一个临时文件（例如 transcription.txt）
    output_file = os.path.join(file_dir, "transcription.txt")

    # 检查文件是否存在
    if not os.path.exists(audio_file):
        logging.error(f"音频文件未找到: {audio_file}")
        raise FileNotFoundError("Audio file not found.")
    else:
        
        #设置忽略警告
        warnings.simplefilter("ignore", UserWarning)
        
        #检查GPU
        check_gpu()
        
        #检查设备类型 是GPU还是CPU
        device = check_device()
        #device="cpu"
        logging.info(f"Using device: {device}")
        
        # 加载模型
        whisper_model = load_whisper(device)
        
        # 转文字
        try:      
            #文件交互
            result=transcribe_audio(audio_file, whisper_model, output_file,device)
        
            # 读取转录结果
            with open(output_file, "r", encoding="utf-8") as f:
                    transcription = f.read()
            
            topic_and_abstract=get_topic_and_abstract(transcription)
            topic_str=topic_and_abstract['topic'].split('：')[1]
            abstract_str=topic_and_abstract['abstract'].split('：')[1]
            
            rawRecognitions=[]
            for rawRecognition in result:
                rawRecognitions.append(RawRecognition(start=time_conversion(rawRecognition.split("\t")[0]),text=rawRecognition.split("\t")[1]))
            
            # 构造响应数据
            response = models.RecordResponse(
                id=int(time.time()),  # 使用时间戳作为唯一标识符
                # 将最后一行记录的开始时间作为总时长 单位 秒
                duration=time_conversion(result[-1].split("\t")[0]),
                topic=topic_str,  
                abstract=abstract_str, 
                raw_recognition=rawRecognitions
                )
            logging.info(f"成功生成响应数据: ID={response.id}")
            return response

        except Exception as e:
            logging.error("处理过程中出现错误：%s", e)
            raise e


        finally:
            # 删除临时文件
            os.remove(audio_file)
            os.remove(output_file)
            logging.info("已删除临时文件")