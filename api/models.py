# 定义请求和响应模型
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
from pydantic import BaseModel


class RecordResponse(BaseModel):
    id: int
    duration: int
    topic: str
    abstract: str
    raw_recognition: list[RawRecognition]

    @classmethod
    def fake(cls):
        return cls(
            id=12345678,
            duration=45 * 60,
            topic="布尔代数",
            abstract="布尔代数是数学的一个分支，它研究的是命题的真值表。",
            raw_recognition=[
                RawRecognition(start=0, end=12, text="什么是布尔值？"),
                RawRecognition(start=13, end=25, text="布尔值有什么用？"),
                RawRecognition(start=26, end=30, text="布尔值有哪两种？"),
                RawRecognition(start=31, end=40, text="什么是命题真值？"),
                RawRecognition(start=41, end=50, text="什么是真值表？"),
                RawRecognition(start=51, end=60, text="真值表有什么用？"),
            ],
        )


class NoteRequest(BaseModel):
    topic: str
    abstract: str
    raw_recognition: list[RawRecognition]


class NoteResponse(BaseModel):
    points: list[Point]

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


class NetworkRequest(BaseModel):
    lectures: list[Lecture]


class NetworkResponse(BaseModel):
    nodes: list[Node]
    links: list[NodeLink]
    categories: list[NodeCategory]

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

class ExportRequest(BaseModel):
    id: int
    topic: str
    abstract: str
    points: list[Point]