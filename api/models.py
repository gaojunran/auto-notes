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
    subtitles: list[Subtitle]
    links: list[Link]
    summary: str

