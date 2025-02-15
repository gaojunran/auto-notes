# -*- coding: utf-8 -*-
"""
This file defines responses and requests
Created on Thu Feb  6 13:27:44 2025
@author: Zeyu Pan
version 2
"""

"""
from api.entities import (
    Lecture,
    Link,
    Node,
    NodeCategory,
    NodeLink,
    NoteRoute,
    Point,
    RawRecognition,
    Subtitle,
)
"""
#BaseModel：用于定义数据模型，强类型校验输入输出数据。
from pydantic import BaseModel

#在api目录下，下行代码可注释掉，选用上面的代码
from entities import RawRecognition, Point, Link, Subtitle,NoteRoute,NodeLink,Lecture,Node,NodeCategory
# 定义请求和响应模型

# 定义record接口响应模型（RecordResponse）
class RecordResponse(BaseModel):
    id: int #id：录音唯一标识。
    duration: int #duration：录音时长（秒）。
    topic: str #topic：录音主题。
    abstract: str #abstract：录音摘要。
    raw_recognition: list[RawRecognition] #raw_recognition：识别的原始内容（一个 RawRecognition 列表）。
    
    # 类方法：生成一个假的 RecordResponse 对象，用于测试或模拟数据
    @classmethod
    def fake(cls):
        return cls(
            id=12345678, # 模拟的录音 ID
            duration=45 * 60, # 模拟的录音时长（45 分钟）
            topic="布尔代数", # 模拟的主题
            abstract="布尔代数是数学的一个分支，它研究的是命题的真值表。", # 模拟的摘要
            raw_recognition=[ # 模拟的原始识别内容
                RawRecognition(start=0, end=12, text="什么是布尔值？"),
                RawRecognition(start=13, end=25, text="布尔值有什么用？"),
                RawRecognition(start=26, end=30, text="布尔值有哪两种？"),
                RawRecognition(start=31, end=40, text="什么是命题真值？"),
                RawRecognition(start=41, end=50, text="什么是真值表？"),
                RawRecognition(start=51, end=60, text="真值表有什么用？"),
            ],
        )

# 定义笔记请求模型（NoteRequest），用于接收生成笔记的请求
class NoteRequest(BaseModel):
    topic: str #topic：笔记主题。
    abstract: str #abstract：笔记摘要。
    raw_recognition: list[RawRecognition] #raw_recognition：识别的原始内容（一个 RawRecognition 列表）。

# 定义笔记响应模型（NoteResponse），用于返回生成的笔记要点
class NoteResponse(BaseModel):
    points: list[Point] #points：笔记要点列表（一个 Point 列表）。

    # 类方法：生成一个假的 NoteResponse 对象，用于测试或模拟数据
    @classmethod
    def fake(cls):
        return cls(
            points=[
                Point(
                    importance=2,
                    name="布尔值",
                    summary="布尔值是逻辑中的基本概念，它只有两个取值：真和假。",
                    links=[
                        Link(
                            name="维基百科",
                            href="https://zh.wikipedia.org/wiki/%E5%B8%83%E5%B0%94%E5%80%BC",
                        ),
                        Link(
                            name="百度百科",
                            href="https://baike.baidu.com/item/%E5%B8%83%E5%B0%94%E5%80%BC",
                        ),
                    ],
                    subtitles=[
                        Subtitle(
                            subtitle="布尔值的定义",
                            md="**布尔值**是逻辑中的基本概念，它只有两个取值：真和假。",
                            raw_recognition=[
                                RawRecognition(start=0, end=12, text="什么是布尔值？"),
                                RawRecognition(
                                    start=13, end=25, text="布尔值有什么用？"
                                ),
                            ],
                        ),
                        Subtitle(
                            subtitle="布尔值的类型",
                            md="布尔值有两种类型：命题真值和命题真值表。",
                            raw_recognition=[
                                RawRecognition(
                                    start=26, end=30, text="布尔值有哪两种？"
                                ),
                                RawRecognition(
                                    start=31, end=40, text="什么是命题真值？"
                                ),
                            ],
                        ),
                    ],
                ),
                Point(
                    importance=3,
                    name="真值表",
                    summary="真值表是指命题的真值对所有可能的取值组合的一种表示。",
                    links=[
                        Link(
                            name="维基百科",
                            href="https://zh.wikipedia.org/wiki/%E7%9C%9F%E5%80%BC%E8%A1%A8",
                        ),
                        Link(
                            name="百度百科",
                            href="https://baike.baidu.com/item/%E7%9C%9F%E5%80%BC%E8%A1%A8",
                        ),
                    ],
                    subtitles=[
                        Subtitle(
                            subtitle="真值表的定义",
                            md="**真值表**是指命题的真值对所有可能的取值组合的一种表示。",
                            raw_recognition=[
                                RawRecognition(start=41, end=50, text="什么是真值表？"),
                                RawRecognition(
                                    start=51, end=60, text="真值表有什么用？"
                                ),
                            ],
                        ),
                    ],
                ),
            ]
        )

# 定义网络请求模型（NetworkRequest），用于接收多个讲座信息
class NetworkRequest(BaseModel):
    lectures: list[Lecture] # lectures：讲座列表（包含多个 Lecture 对象）

# 定义网络响应模型（NetworkResponse），用于返回网络图数据，包括节点、连接和分类
class NetworkResponse(BaseModel):
    nodes: list[Node] # nodes：节点列表（包含多个 Node 对象）
    links: list[NodeLink] # links：节点连接列表（包含多个 NodeLink 对象）
    categories: list[NodeCategory] # categories：节点分类列表（包含多个 NodeCategory 对象）

     # 类方法：生成一个假的 NetworkResponse 对象，用于测试或模拟数据
    @classmethod
    def fake(cls):
        return cls(
            nodes=[
                Node(
                    name="布尔代数", category=0, size=5, route=NoteRoute(id=12345678)
                ),  # topic
                Node(
                    name="布尔值",
                    category=0,
                    size=2,
                    route=NoteRoute(id=12345678, point="布尔值"),
                ),  # point
                Node(
                    name="真值表",
                    category=0,
                    size=3,
                    route=NoteRoute(id=12345678, point="真值表"),
                ),  # point
                Node(
                    name="另一个topic",
                    category=1,
                    size=4,
                    route=NoteRoute(id=12345679),
                ),  # point
                Node(
                    name="另一个point",
                    category=1,
                    size=1,
                    route=NoteRoute(id=12345679, point="另一个point"),
                ),  # point
            ],
            links=[
                NodeLink(source="布尔代数", target="真值表", weight=1),
                NodeLink(source="布尔代数", target="布尔值", weight=2),
                NodeLink(source="真值表", target="另一个point", weight=1),
                NodeLink(source="另一个topic", target="另一个point", weight=4),
            ],
            categories=[
                NodeCategory(idx=0, name="布尔代数"),
                NodeCategory(idx=1, name="另一个topic"),
            ],
        )

# 定义导出请求模型（ExportRequest），用于请求导出笔记
class ExportRequest(BaseModel):
    id: int
    topic: str
    abstract: str
    points: list[Point]