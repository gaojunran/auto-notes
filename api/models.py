from pydantic import BaseModel, Field


class RawRecognition(BaseModel):
    start: int
    end: int
    text: str

class Link(BaseModel):
    name: str
    href: str

class Subtitle(BaseModel):
    subtitle: str
    md: str
    raw_recognition: list[RawRecognition]

class Point(BaseModel):
    name: str
    importance: int = Field(ge=1, le=5)
    subtitles: list[Subtitle] | None = None
    links: list[Link] | None = None
    summary: str | None = None

class NodeCategory(BaseModel):
    idx: int
    name: str

class NodeLink(BaseModel):
    source: int
    target: int
    weight: int = Field(ge=1, le=5)

class Node(BaseModel):
    idx: int
    name: str
    category: int
    size: int = Field(ge=1, le=5)
    route: str = Field(pattern=r'/detail/notes/\d+.*')

class Lecture(BaseModel):
    id: int
    topic: str
    points: list[Point]