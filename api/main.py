import time

from fastapi import FastAPI, UploadFile
from pydantic import BaseModel

from models import RawRecognition, Point, Link, Subtitle

app = FastAPI()


# 定义请求和响应模型
class RecordResponse(BaseModel):
    id: int
    duration: int
    topic: str
    abstract: str
    raw_recognition: list[RawRecognition]

class NoteRequest(BaseModel):
    topic: str
    abstract: str
    raw_recognition: list[RawRecognition]

class NoteResponse(BaseModel):
    points: list[Point]

# class ThoughtRequest(BaseModel):
#     notes: str
#     num: int
#
# class Question(BaseModel):
#     question: str | list[str]
#     answer: str
#     analysis: str | None = None
#     knowledge: list[str] | None = None
#
# class ThoughtResponse(BaseModel):
#     questions: list[Question]
#
# class ExerciseRequest(BaseModel):
#     notes: str
#     num: int
#
# class ExerciseResponse(BaseModel):
#     questions: list[Question]


@app.get("/test", response_model=str)
async def test():
    return "Hello, World!"

@app.post("/record", response_model=RecordResponse)
async def post_record(file: UploadFile):
    time.sleep(2) # 模拟延时
    return RecordResponse(
        id=int(time.time()),
        duration=45*60,
        topic="布尔代数",
        abstract="布尔代数是数学的一个分支，它研究的是命题的真值表。",
        raw_recognition=[
            RawRecognition(start=0, end=12, text="命题的真值表是...."),
            RawRecognition(start=13, end=25, text="命题的真值表有几种形式？"),
        ]
    )


@app.post("/note", response_model=NoteResponse)
async def get_note(note: NoteRequest):
    time.sleep(2)  # 模拟延时
    return NoteResponse(
        points=[
            Point(importance=2, name="布尔值", summary="布尔值是逻辑中的基本概念，它只有两个取值：真和假。", links=[
                Link(name="维基百科", href="https://zh.wikipedia.org/wiki/%E5%B8%83%E5%B0%94%E5%80%BC"),
                Link(name="布尔代数", href="https://zh.wikipedia.org/wiki/%E5%B8%83%E5%B0%94%E4%BB%A3%E6%95%B0"),
            ], subtitles=[
                Subtitle(subtitle="真值表",
                         md="**真值表**是指一个命题的真值对各个可能的取值组合的一种表示。 真值表的形式有很多种，但最常见的形式是用真值或假值来表示命题的真值。",
                         raw_recognition=[
                             RawRecognition(start=21 * 60, end=21 * 60 + 12, text="真值表的形式有几种形式？"),
                             RawRecognition(start=21 * 60 + 13, end=21 * 60 + 25, text="真值表有几种形式？"),
                         ]
                )
            ])
        ]
    )

# @app.post("/thought", response_model=ThoughtResponse)
# async def get_thought(thought: ThoughtRequest):
#     time.sleep(2) # 模拟延时
#     return FAKE_THOUGHT_RESPONSE
#
# @app.post("/exercise", response_model=ExerciseResponse)
# async def get_exercise(exercise: ExerciseRequest):
#     time.sleep(2) # 模拟延时
#     return FAKE_EXERCISE_RESPONSE
