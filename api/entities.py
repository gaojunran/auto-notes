# -*- coding: utf-8 -*-
"""
This file defines some data structures
Created on Thu Feb  6 13:46:07 2025
@author: Zeyu Pan
version 3
"""
from pydantic import BaseModel, Field

"""
#功能:表示一段识别内容的结构。
#用途：
#可用于表示录音中某一段的文字内容及其时间范围。
#适合记录转录结果中的片段。
"""
class RawRecognition(BaseModel):
    start: int #start：起始时间点（秒）。
    end: int|None=None #end：结束时间点（秒）。
    text: str|None=None #text：识别的文本内容。

"""
#功能:表示与笔记相关的链接信息。
#用途：
#提供与笔记内容相关的参考资料。
#链接信息通常用于丰富笔记内容的上下文。
"""
class Link(BaseModel):
    name: str #name：链接的名称或描述。
    href: str #href：链接地址（URL）。

"""
#功能:表示笔记中的一个子标题及其相关内容。
#用途：
#细分笔记的内容，每个子标题下包含与之相关的解释和识别内容。
"""
class Subtitle(BaseModel):
    subtitle: str #subtitle：子标题的文本。
    md: str #md：与子标题相关的 Markdown 格式文本（比如说明或示例）。
    raw_recognition: list[RawRecognition] #raw_recognition：一个 RawRecognition 列表，用于表示与该子标题关联的原始识别片段。

"""
#功能:表示笔记中的一个路线，用于链接某个要点。
#用途：
#该类用于定义笔记路线，通常表示某个要点的识别时间点及其相关的标题信息。
"""
class NoteRoute(BaseModel):
    id: int  # id：笔记路线的唯一标识符。
    point: str | None = None  # point：关联的要点名称（可选）。指明该路线所属的要点。

"""
#功能
#表示笔记中的一个核心要点。
#用途：
#代表一个笔记的核心知识点，包含详细的说明、相关链接和重要性。
#代码整体逻辑
#面向 API 的数据结构：
#每个类通过继承 BaseModel 提供了数据类型校验和序列化能力，确保输入和输出数据结构的正确性。
#层次化组织笔记内容：
#顶层是 Point 类，表示笔记的核心要点。
#每个 Point 由多个 Subtitle（子标题）和 Link（参考链接）组成。
#每个 Subtitle 又关联多个 RawRecognition，表示与子标题相关的原始识别内容。
#字段验证：
#例如 importance 字段使用了 Field(ge=1, le=5)，确保其值在 1 到 5 的范围内。
#Markdown 支持：
#Subtitle 中的 md 字段允许使用 Markdown 格式内容，方便生成更加丰富的展示页面。
"""
class Point(BaseModel):
    name: str #name：要点的名称。
    importance: int = Field(ge=1, le=5) #importance：要点的重要程度，范围为 1-5（通过 Field 校验）。
    subtitles: list[Subtitle] #subtitles：与该要点相关的子标题列表（类型为 Subtitle）。
    links: list[Link] #links：与该要点相关的链接列表（类型为 Link）。
    summary: str #summary：该要点的简要总结。

"""
#功能:表示节点类别的结构，用于组织不同类型的节点。
#用途：
#该类用来定义节点的类别，便于分类和组织。
"""
class NodeCategory(BaseModel):
    idx: int  # idx：类别的唯一标识符。
    name: str  # name：类别名称。描述该类别的名字。

"""
#功能:表示节点之间的连接关系。
#用途：
#定义节点间的连接及其权重，用于图形化表示节点的联系。
"""
class NodeLink(BaseModel):
    source: str  # source：起始节点的标识符。
    target: str  # target：目标节点的标识符。
    weight: int = Field(ge=1, le=5)  # weight：连接的权重，范围为 1 到 5，用于表示连接的强度或重要性。

"""
#功能:表示图中的节点。
#用途：
#该类用于定义图中的节点，包含节点的基本信息、类别、大小以及连接信息。
"""
class Node(BaseModel):
    idx: int | None = None  # idx：节点的唯一标识符（可选）。若未指定则为 None。
    name: str  # name：节点的名称。该节点的标题或名称。
    category: int  # category：节点所属的类别，使用整数值表示类别 ID。
    size: int = Field(ge=1, le=5)  # size：节点的大小，范围为 1 到 5，通常用于表示该节点的重要性或视觉大小。
    route: NoteRoute  # route：该节点的关联路线。链接到某个笔记要点。

"""
#功能:表示一门讲座的结构。
#用途：
#该类用于定义一个讲座，包含讲座的主题以及该讲座中涉及的多个笔记要点。
"""
class Lecture(BaseModel):
    id: int  # id：讲座的唯一标识符。
    topic: str  # topic：讲座的主题或标题。
    points: list[Point]  # points：该讲座所涉及的要点列表。每个要点代表讲座中的一个核心知识点。

"""
#附：整体数据模型的关系图
Lecture
├── id: int
├── topic: str
└── points: list[Point]
    ├── name: str
    ├── importance: int
    ├── subtitles: list[Subtitle] | None
    │   ├── subtitle: str
    │   ├── md: str
    │   └── raw_recognition: list[RawRecognition]
    │       ├── start: int
    │       ├── end: int
    │       └── text: str
    ├── links: list[Link] | None
    │   ├── name: str
    │   └── href: str
    └── summary: str | None
       
Node
├── idx: int | None
├── name: str
├── category: int
├── size: int
└── route: NoteRoute
    ├── id: int
    └── point: str | None

NodeCategory
├── idx: int
└── name: str

NodeLink
├── source: str
├── target: str
└── weight: int

RawRecognition
├── start: int
├── end: int
└── text: str

Link
├── name: str
└── href: str

Subtitle
├── subtitle: str
├── md: str
└── raw_recognition: list[RawRecognition]

NoteRoute
├── id: int
└── point: str | None

Point
├── name: str
├── importance: int
├── subtitles: list[Subtitle] | None
├── links: list[Link] | None
└── summary: str | None

解释：
Lecture 是最顶层的结构，包含讲座的信息（id、topic）以及一系列 Point（要点）。
Point 表示一个笔记要点，包含要点的名称、重要性、子标题、链接和总结等信息。
Subtitle 是与某个 Point 相关的小节或子标题，包含文本和 Markdown 格式内容以及原始识别内容 RawRecognition。
Link 提供与该要点相关的参考链接。
RawRecognition 是一个基础类，表示录音中的一段识别文本，包含开始时间、结束时间和文本内容。
Node 是图中节点的表示，包含节点的基本信息，如名称、类别、大小等，还关联一个 NoteRoute（笔记路线），用于指向某个笔记要点。
NodeCategory 定义节点的类别，区分不同类型的节点。
NodeLink 表示节点之间的连接，包含源节点、目标节点和连接权重。
NoteRoute 描述节点的路线，包含一个 ID 和关联的笔记要点名称。
数据模型关系
Lecture -> 包含多个 Point
Point -> 包含多个 Subtitle 和 Link
Subtitle -> 包含多个 RawRecognition
Node -> 通过 NoteRoute 关联到 Point
NodeLink 用于连接不同的 Node
NodeCategory 用于分类 Node。
"""