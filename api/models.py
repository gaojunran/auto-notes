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
                    name="Propositional Logic", category=0, size=5, route=NoteRoute(id=1),
                ),  # topic
                Node(
                    name="Predicate Logic", category=1, size=5, route=NoteRoute(id=2),
                ),  # topic
                Node(
                    name="Set", category=2, size=5, route=NoteRoute(id=3),
                ),  # topic
                Node(
                    name="Functions", category=3, size=5, route=NoteRoute(id=4),
                ),  # topic
                Node(
                    name="Sequences and Summations", category=4, size=5, route=NoteRoute(id=5),
                ),  # topic
                Node(
                    name="Matrices", category=5, size=5, route=NoteRoute(id=6),
                ),  # topic
                Node(
                    name="The Language of Propositions", category=0, size=4, route=NoteRoute(id=7),
                ),
                Node(
                    name="Applications of Proposition Logic", category=0, size=3, route=NoteRoute(id=8),
                ),
                Node(
                    name="Logical Equivalences", category=0, size=3, route=NoteRoute(id=9),
                ),
                Node(
                    name="The Language of Quantifiers", category=1, size=4, route=NoteRoute(id=10),
                ),
                Node(
                    name="Describing Sets", category=2, size=3, route=NoteRoute(id=11),
                ),
                Node(
                    name="Subsets and Set Equality", category=2, size=4, route=NoteRoute(id=12),
                ),
                Node(
                    name="Cardinality of Sets", category=2, size=4, route=NoteRoute(id=13),
                ),
                Node(
                    name="Set Operations", category=2, size=4, route=NoteRoute(id=14),
                ),
                Node(
                    name="Membership Tables", category=2, size=5, route=NoteRoute(id=15),
                ),
                Node(
                    name="Injection, Surjection, Bijection", category=3, size=4, route=NoteRoute(id=16),
                ),
                Node(
                    name="Inverse Function", category=3, size=2, route=NoteRoute(id=17),
                ),
                Node(
                    name="Function Composition", category=3, size=4, route=NoteRoute(id=18),
                ),
                Node(
                    name="Recurrence Relations", category=4, size=3, route=NoteRoute(id=19),
                ),
                Node(
                    name="Summations", category=4, size=3, route=NoteRoute(id=20),
                ),
                Node(
                    name="Matrix Arithmetic", category=5, size=2, route=NoteRoute(id=21),
                )
            ],
            links=[
                # Centralized
                NodeLink(source="Propositional Logic", target="The Language of Propositions", weight=1),
                NodeLink(source="Propositional Logic", target="Applications of Proposition Logic", weight=1),
                NodeLink(source="Propositional Logic", target="Logical Equivalences", weight=1),
                NodeLink(source="Predicate Logic", target="The Language of Quantifiers", weight=1),
                NodeLink(source="Set", target="Describing Sets", weight=1),
                NodeLink(source="Set", target="Subsets and Set Equality", weight=1),
                NodeLink(source="Set", target="Cardinality of Sets", weight=1),
                NodeLink(source="Set", target="Set Operations", weight=1),
                NodeLink(source="Set", target="Membership Tables", weight=1),
                NodeLink(source="Functions", target="Injection, Surjection, Bijection", weight=1),
                NodeLink(source="Functions", target="Inverse Function", weight=1),
                NodeLink(source="Functions", target="Function Composition", weight=1),
                NodeLink(source="Sequences and Summations", target="Recurrence Relations", weight=1),
                NodeLink(source="Sequences and Summations", target="Summations", weight=1),
                NodeLink(source="Matrices", target="Matrix Arithmetic", weight=1),

                # Distributed
                NodeLink(source="The Language of Propositions", target="The Language of Quantifiers", weight=2),
                NodeLink(source="Applications of Proposition Logic", target="Membership Tables", weight=2),
                NodeLink(source="Set Operations", target="Membership Tables", weight=2),
                NodeLink(source="Function Composition", target="Inverse Function", weight=2),
                NodeLink(source="The Language of Propositions", target="Describing Sets", weight=2),
                NodeLink(source="Subsets and Set Equality", target="Set Operations", weight=2),
                NodeLink(source="Cardinality of Sets", target="Set Operations", weight=2),
                NodeLink(source="The Language of Propositions", target="Recurrence Relations", weight=2),
                NodeLink(source="The Language of Quantifiers", target="Recurrence Relations", weight=2),
                NodeLink(source="Injection, Surjection, Bijection", target="Applications of Proposition Logic", weight=2),
                NodeLink(source="Matrix Arithmetic", target="Set Operations", weight=2),
            ],
            categories=[
                NodeCategory(idx=0, name="Propositional Logic"),
                NodeCategory(idx=1, name="Predicate Logic"),
                NodeCategory(idx=2, name="Set"),
                NodeCategory(idx=3, name="Functions"),
                NodeCategory(idx=4, name="Sequences and Summations"),
                NodeCategory(idx=5, name="Matrices"),
            ],
        )

class ExportRequest(BaseModel):
    id: int
    topic: str
    abstract: str
    points: list[Point]