# -*- coding: utf-8 -*-
"""
This file provides help methods for the note API
Created on Sun Feb  9 18:31:24 2025
@author: Zeyu Pan
version 3
"""
from langchain_core.messages import SystemMessage

import locale
locale.getpreferredencoding = lambda: "UTF-8"

#记录日志
import myLogging

#引入响应和请求
from models import NoteResponse

# 获取默认的日志记录器
logging = myLogging.default_logger

from entities import RawRecognition,Subtitle,Link,Point

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

import json
        
"""
生成笔记
"""
def getNote(model_name:str,url:str,record_text:list[RawRecognition]):
    
    try:
        logging.info("开始生成笔记...")
        
        # 初始化ChatOpenAI模型，指定模型名称、API基础地址和最大token数。
        model_str = ChatOpenAI(
            model=model_name,
            openai_api_base=url,
            api_key="0f78283e98d641af831083f72612950b.ZyRMh52V3a4LmmRy",
            max_tokens=4095, # 最大token数，限制输出的长度
        )
        logging.info(f"ChatOpenAI 模型 {model_name} 初始化成功")
        
        # 先格式化 record_text 变成元组列表
        #formatted_text = formatText(record_text)
        formatted_text=record_text

        # 构建一个消息模板，定义聊天的格式
        prompt_template_str = ChatPromptTemplate.from_messages(
            [   #SystemMessage(content="hello"),
                ('system','用户以列表形式输入一堂课的录音文本，列表中每一项前半部分为这句话的时间，后半部分为这句话的文本，你被要求先优化识别错误的内容，然后根据处理后的文本，以文本形式输出一个课堂笔记，内容是：1.课程主题。2.课程摘要。3.详细的知识点笔记(每个知识点包含名称、重要程度（整数1-5，根据我给你的重要程度规则结合你自己这门学科的知识给出）、然后由子要点阐述解释或例子（子要点如定义、应用、证明等），每个子要点的标题前要有这个概念在录音文本中第一次被提到的时间（即这个子要点的开始时间,要仔细审查），每个要点后附这个子要点对应的全部文本，即不要有任何改动的原文本(注意例题也算一个子要点)））。4.几个关键词及对应的参考网站。（可以分开写但要确保覆盖全部时间全部要点）'
                          '重要程度规则如下：5.科目重点：这门课的核心内容，教师强调为这门科目的最重要内容之一，用了超过20分钟详细讲解该知识点的推导过程、应用场景及例题剖析，需要掌握复杂灵活应用的方法的知识点，如在高等数学中的微积分基本定理、线性代数中矩阵的秩，应用贯穿整个科目。课程重点最多只有一个；4.单元重点：难度及重要性不如课程重点，但与本单元核心内容紧密相关，教师多次强调重要/考试重点等的知识点，单知识点讲解时长超过10分钟，同时会涉及一定难度的灵活应用，要求学生熟练掌握并能较好运用的知识点，如线性代数中的矩阵乘法部分，是理解后续矩阵特征值、特征向量等知识的基础；3.基础重点：是后续学习其他重要知识的基础铺垫，教师讲解时长不到十分钟，通常会结合简单例题进行说明，要求学生理解并能够进行基础应用，为深入学习后续内容必备的知识点，如高等数学的极限内容，是后续学习导数、积分等知识的必备基础；2. 次要知识点：对整体知识架构有一定补充作用，教师讲解时间相对较短，可能仅提及概念或简单提及应用场景，一般不会深入展开应用，要求学生了解即可的知识点,如大学物理中带电粒子在电场和磁场中运动举例（质谱仪、回旋加速器等），仅要求了解应用场景；1.了解知识点：在本节课中提及较少，与核心内容关联性较弱，仅作为拓展信息或背景知识，无需花费过多精力去深入探究的知识点，如某个领域的发展历程；重要程度为1也可能是难度过大当前无需掌握的知识点，如高等数学中含参变量的积分。'
                          '示例如下：主题：二阶行列式和三阶行列式的定义及其计算；摘要：本节课首先通过一个二元一次方程组的例子，引出了二阶行列式的定义和计算方法。接着，介绍了三阶行列式的定义和计算方法，包括对角线法则。最后，讨论了特殊的行列式。'
                          '详细的知识点笔记：1. 二阶行列式的定义与计算 (重要程度：5)：（00:01）二阶行列式的定义：一个方程组的系数矩阵的主对角线元素之积，即对角线元素的乘积；（03：52）二阶行列式的计算方法：利用二阶行列式的定义，将方程组的系数矩阵化为上三角矩阵，再利用对角线元素的乘积求和。2. 三阶行列式的定义与计算 (重要程度：5)：（05：44）三阶行列式的定义：一个方程组的系数矩阵的主对角线元素之积，即对角线元素的乘积；（08：36）三阶行列式的计算方法：利用代数余子式的性质，利用三阶行列式的定义，将方程组的系数矩阵化为上三角矩阵，再利用对角线元素的乘积求和。3.特殊行列式（重要程度：3）：（15:03)上三角行列式：是主对角线以下的元素均为零的行列式，其值等于主对角线元素的乘积;（16:27)下三角行列式：主对角线以上的元素均为零的行列式，其值等于主对角线元素的乘积。关键词及参考网站：行列式 - 维基百科：https://zh.wikipedia.org/wiki/%E8%A1%8C%E5%88%97%E5%BC%8F；线性代数 - 可汗学院：https://zh.khanacademy.org/math/linear-algebra'
                          ),
                # 用户消息（此处用户输入的内容就是一堂课的录音文本，这将被模型用来生成课堂笔记）
                ('human','{formatted_text}') 
            ]
        )
        logging.info("消息模板构建成功")
        
        
        # 将消息模板与模型连接，创建一个处理流程链（chain）
        chain_str = prompt_template_str|model_str
        
        #logging.info(formatted_text[:5])
            
        note_text_all = chain_str.invoke(input = {'formatted_text': formatted_text})

        modelFinishReason=note_text_all.response_metadata['finish_reason']
        note_text = note_text_all.content
        
        #if isinstance(note_text, bytes):
        #    note_text = note_text.decode('utf-8', errors="ignore")  # 解码成 UTF-8
        
        logging.info(f"笔记生成成功, 模型输出token数：{len(note_text)}，内容如下：\n{note_text}")
        
        if modelFinishReason=='length':
            model_str = ChatOpenAI(
                model="glm-4-long",
                openai_api_base=url,
                api_key="0f78283e98d641af831083f72612950b.ZyRMh52V3a4LmmRy",
                max_tokens=4095,
                # response_format={'type':'json_object'}
            )
            chain_str = prompt_template_str | model_str
            note_text_all = chain_str.invoke(input={'record_text': record_text})
            note_text = note_text_all.content
            logging.info("token超限，模型(长文本)运行成功")
            logging.info(note_text)

        note_text = note_text.replace('{', '{{').replace('}', '}}')
        return note_text
    except Exception as e:
        logging.error(f"生成笔记失败: {e}")
        raise e

"""
检查模型
"""
def checkModel(note_text):
    model_name='glm-4-air-0111'
    
    #主要是根据人文类定的，数学类的话由于有很多公式token会虚多，很容易就切换到long了，效果下降，之后再想想怎么办
    #if len(note_text) > 1000:
    #    model_name='glm-4-long'
    if len(note_text) > 4000:#纯摆设 符号很多的数学类待考虑 口语化的课程1000就会超限
        model_name='glm-4-long'
        
    return model_name

# 生成响应
def generateResponse(model_name: str, url: str, note_text: str):
    """
    将课堂笔记转换为符合 NoteResponse 结构的 JSON 数据。

    参数：
    - model_name (str): ChatOpenAI 使用的模型名称。
    - url (str): OpenAI API 的基础 URL。
    - note_text (str): 课堂笔记的文本内容。

    返回：
    - dict: 符合 NoteResponse 结构的字典，包含课程主题、知识点、摘要、关键词等信息。
    """

    try:
        logging.info("开始生成 JSON 响应...")

        # 初始化 ChatOpenAI 模型
        model_json = ChatOpenAI(
            model=model_name,
            openai_api_base=url,
            api_key="0f78283e98d641af831083f72612950b.ZyRMh52V3a4LmmRy",
            max_tokens=4095,
            temperature=0,
        )
        logging.info(f"ChatOpenAI 模型 {model_name} 初始化成功")

        # 定义系统提示，描述 JSON 结构
        model_json_message = ("接下来把用户输入的课堂笔记进行拆分并输出一个.json文件代码(不是让你写一个用于转换成json的程序，而是直接输出json文件)，不分行，除了代码什么都不要，包含：1.课程主题。2.详细的知识点笔记(知识点是由字典组成的列表，每个知识点包含名称、重要程度（整数1-5，5代表最重要）、子要点（每一个知识点要有对应的解释或例子，由子要点组织，即子要点是知识点内容的具体阐述、该知识点开始时间以及这个知识点对应的全部文本，子要点的名字要是一个简洁的词语或短语）；子要点也是由字典组成的列表，键和值用markdown格式，键用一级标题，值可以适当加粗或斜体等）、以字典列表组织的每个子要点对应的开始时间。3.关键词及对应的参考网站。4.课程摘要。示例如下："
                           #"{{'theme'：'二阶和三阶行列式的定义及其计算方法', 'points'：[{{'name：'#二阶行列式','importance':4, 'subtitles'：[{{'#定义':'二阶行列式由两个正项相乘减去两个数负项相乘得到。'}}, {{'#应用'：'解二元一次方程'}}]}},[{{'name：'#特殊行列式','importance':2, 'subtitles'：[{{'#上三角行列式':'所有主对角以下的元素**为零**的行列式。'}}, {{'#下三角行列式'：'有主对角以上的元素**为零**的行列式'}}]}}],"
                           "{{'theme'：'二阶和三阶行列式的定义及其计算方法', 'points'：[{{'name：'#二阶行列式','importance':4, 'subtitles'：[{{'subtitle':'#定义','md':'**二阶行列式**由两个正项相乘减去两个数负项相乘得到。','raw_recognition':[{{'start':00:00,'end':01:58}}]}},"
                             # " {{'subtitle':'#应用','md':'解二元一次方程。',raw_recognition':[{{'start':01:58,'end':03:00]}}]}}]}}],[{{'name：'#特殊行列式','importance':2, 'subtitles'：[{{'subtitle':'#上三角行列式','md':{{'所有**主对角以下**的元素**为零**的行列式。'}},raw_recognition':[{{'start':03:00,'end':04:00,''text':'我们看这个题，而且我们来呗。啊。第一个这么想，第二个政策呢？咱甭写了，因为它有零。第三个正向呢？对吧？也有零吗？第一个负向是不是有零啊？第二个负向，这没有礼貌。第三个附向也有理吗？也有理吗？那就这么着了呗，对吧？那这个行列式啊，我们其实是有一个特殊的名字，哈？它其实是叫一个上三角。行列式。'}}],'"
                             "{{'subtitle':'#应用','md':'解二元一次方程。',raw_recognition':[{{'start':01:58,'end':03:00]}}]}}]}}],"
                             "[{{'name：'#特殊行列式','importance':2, 'subtitles'：[{{'subtitle':'#上三角行列式','md':{{'所有**主对角以下**的元素**为零**的行列式。'}},raw_recognition':[{{'start':03:00,'end':04:00}}]}},'"
                             # "{{'subtitle':'#下三角行列式','md':'所有主对角以上的元素**为零**的行列式'，raw_recognition':[{{'start':04:00,'end':05:00,'text':'我们后边还会讲n结的。哈？那么，它的这个定义也非常简单。就是，你看，这不是上面有东西吗？下边就是没东西嘛，下边全都零嘛。这种就叫做上三段行业是它的结果啊。就等于主标线员不想省就完事了。那再来一个这个呢？叫做一个下三角行列式啊。下半年好像是它的主要呢。'}}]}}],"
                             "{{'subtitle':'#下三角行列式','md':'所有主对角以上的元素**为零**的行列式'，raw_recognition':[{{'start':04:00,'end':05:00]}}]}}]}}],"
                           "'links':[{{'name'：'MIT OpenCourseWare'，'href'：'https://ocw.mit.edu/courses/mathematics/18-06-linear-algebra-spring-2010'}}, {{'name'：'Wolfram MathWorld'，'href'：'hhttps://mathworld.wolfram.com/Determinant.html'}}],"
                             "'summary'：'二阶行列式由两个正项相乘减去两个数负项相乘得到。三阶行列式由九个元素组成，计算时需要考虑三个正项和三个负项。正项是沿着主对角线、副对角线以及从左上角到右下角的对角线上的元素乘积。负项是沿着主对角线、副对角线以及从右上角到左下角的对角线上的元素乘积。三阶行列式的计算使用对角线法则，将三阶行列式展开为三个正项和三个负项的和。特殊行列式包括上三角行列式、下三角行列式和对角行列式。'}})")


        # 构建 Prompt 模板
        prompt_template_json = ChatPromptTemplate.from_messages(
            [
                ('system',model_json_message),
                ('human', note_text)  # 课堂笔记内容
            ]
        )
        logging.info("JSON 结构化提示词构建成功")

        # 连接 Prompt 和 ChatOpenAI
        chain_json = prompt_template_json | model_json

        # 执行推理，生成 JSON 结果
        json_text_all = chain_json.invoke({})
        json_text = json_text_all.content
        logging.info("模型推理完成，成功生成 JSON")
        
        modelFinishReason=json_text_all.response_metadata['finish_reason']
        
        if modelFinishReason=='length':
            model_json = ChatOpenAI(
                model="glm-4-long",
                openai_api_base=url,
                api_key="0f78283e98d641af831083f72612950b.ZyRMh52V3a4LmmRy",
                max_tokens=4095,
                temperature=0
                # response_format={'type':'json_object'}
            )
            prompt_template_json = ChatPromptTemplate.from_messages(
                [
                    ('system', model_json_message),
                    ('human', note_text)
                ]
            )
            chain_json = prompt_template_json | model_json
            json_text_all = chain_json.invoke({})
            json_text = json_text_all.content
            logging.info("token超限，模型(长文本)运行成功")
            modelFinishReason =json_text_all.response_metadata['finish_reason']

        # 清理 JSON 代码块
        json_text = json_text.strip().replace('```json', '').replace('```', '')
        
        logging.info(json_text)
        
        #将str类型的json_text 解析为字典
        json_dict=json.loads(json_text)
        
        noteResponse=convert_json_to_note_response(json_dict)
        
        noteResponse_dict = noteResponse.__dict__

        # 验证 noteResponse 是否符合 NoteResponse 结构
        note_response = NoteResponse(**noteResponse_dict)

        logging.info("最终 NoteResponse 结构校验通过")
        return note_response

    except Exception as e:
        logging.error(f"生成 JSON 失败: {e}")
        raise e

"""
获取响应
"""
def getResponse(note:list[RawRecognition]):
    
    try:
        # 设置模型及网址
        model_name='glm-4-air-0111'
        base_url="https://open.bigmodel.cn/api/paas/v4/"
        
        #生成笔记
        note_text=getNote(model_name,base_url,note)
        
        #检查模型
        model_name=checkModel(note_text)    
        
        #生成响应
        return generateResponse(model_name,base_url,note_text)
    except Exception as e:
        raise e

"""
转换时间格式为秒数
"""
def convert_time_to_seconds(time_str):
    if time_str:
        # 假设输入格式为 "mm:ss" 或 "hh:mm:ss"
        parts = time_str.split(":")
        if len(parts) == 2:  # mm:ss 格式
            minutes, seconds = map(int, parts)
            return minutes * 60 + seconds
        elif len(parts) == 3:  # hh:mm:ss 格式
            hours, minutes, seconds = map(int, parts)
            return hours * 3600 + minutes * 60 + seconds
    return 0  # 默认返回0秒

"""
将JSON格式转化为NoteResponse
"""
def convert_json_to_note_response(json_data):
    points = []
    
    # 遍历 JSON 中的每个要点
    for point_data in json_data["points"]:
        subtitles = []
        
        # 遍历每个要点的子标题
        for subtitle_data in point_data["subtitles"]:
            raw_recognition = [
                RawRecognition(start=convert_time_to_seconds(rec["start"])) 
                for rec in subtitle_data["raw_recognition"]
            ]
            subtitle = Subtitle(
                subtitle=subtitle_data["subtitle"],
                md=subtitle_data["md"],
                raw_recognition=raw_recognition
            )
            subtitles.append(subtitle)
        
        links = [
            Link(name=link["name"], href=link["href"]) for link in json_data.get("links", [])
        ]
        
        point = Point(
            name=point_data["name"],
            importance=point_data["importance"],
            subtitles=subtitles,
            links=links,
            summary=point_data.get("summary", "")
        )
        
        points.append(point)
    
    # 创建 NoteResponse 实例
    note_response = NoteResponse(points=points)
    
    return note_response

import tempfile
import os
        
"""
将list[RawRecognition]格式化为元组列表（第一项为时间，第二项为文本）
新代码无需格式化
"""
def formatText(record_text: list):
    try:
        # 创建一个临时文件
        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
            # 格式化并写入文件
            for record in record_text:
                start = record.start
                text = record.text.replace('\n', '')  # 去除文本中的换行符
                
                # 数学计算将秒转换为 'HH:MM:SS' 格式
                hours = start // 3600
                minutes = (start % 3600) // 60
                seconds = start % 60
                formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"  # 格式化为两位数
                temp_file.write(f"{formatted_time}\t{text}\n")

            temp_file_path = temp_file.name  # 获取临时文件路径
        
        # 读取临时文件内容
        with open(temp_file_path, 'r', encoding='utf-8') as f:
            record_text_l = f.readlines()

        # 删除临时文件
        os.remove(temp_file_path)

        # 处理每一行，并将其转换为所需的元组格式
        result = []
        for line in record_text_l:
            line = line.replace('\n', '')  # 去掉换行符
            parts = line.split('\t')  # 按照 Tab 分隔时间和文本
            if len(parts) == 2:
                result.append((parts[0], parts[1]))  # 添加到结果列表中

        return result

    except Exception as e:
        logging.error(f"处理文本时发生错误: {e}")
        raise e