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


class NoteRoute(BaseModel):
    id: int
    point: str | None = None


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
    source: str
    target: str
    weight: int = Field(ge=1, le=5)


class Node(BaseModel):
    idx: int | None = None
    name: str
    category: int
    size: int = Field(ge=1, le=5)
    route: NoteRoute


class Lecture(BaseModel):
    id: int
    topic: str
    points: list[Point]
