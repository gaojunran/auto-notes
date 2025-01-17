import time

from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import List, Annotated
import json

app = FastAPI()


# 定义请求和响应模型
class RecordResponse(BaseModel):
    id: int
    duration: int
    topic: str
    abstract: str
    raw_recognition: str

class NoteRequest(BaseModel):
    topic: str
    raw_recognition: str

class NoteResponse(BaseModel):
    notes: str

class ThoughtRequest(BaseModel):
    notes: str
    num: int

class Question(BaseModel):
    question: str
    answer: str
    analysis: str | None = None
    knowledge: list[str] | None = None

class ThoughtResponse(BaseModel):
    questions: list[Question]

class ExerciseRequest(BaseModel):
    notes: str
    num: int

class ExerciseResponse(BaseModel):
    exercises: list[Question]

# 伪造的数据，由大模型生成，仅供测试使用
FAKE_RECORD_RESPONSE = {
    "id": 2,
    "duration": 120,
    "topic": "人工智能",
    "abstract": "本文介绍了人工智能的基本概念和应用。",
    "raw_recognition": "00:00:00 -> 00:02:00 人工智能是计算机科学的一个分支，主要研究如何使计算机具有智能..."
}

FAKE_NOTE_RESPONSE = {
    "notes": """
# 人工智能
    
## 什么是**人工智能**？
    
人工智能是计算机科学的一个分支。
    
...
    """
}

FAKE_THOUGHT_RESPONSE = {
    "questions": [
        {
            "question": "什么是人工智能？",
            "answer": "人工智能是计算机科学的一个分支。",
            "analysis": "本题考查对人工智能基本概念的理解。",
            "knowledge": ["人工智能", "计算机科学"]
        }
    ]
}

FAKE_EXERCISE_RESPONSE = {
    "exercises": [
        {
            "question": ["人工智能有哪些应用领域？", "自然语言处理", "图像识别", "机器学习"],
            "answer": "自然语言处理", # 单选
            "knowledge": ["人工智能", "应用领域"]
        }
    ]
}

# 定义路由
@app.post("/record", response_model=RecordResponse)
async def post_record(file: UploadFile):
    time.sleep(2) # 模拟延时
    return FAKE_RECORD_RESPONSE

@app.post("/note", response_model=NoteResponse)
async def get_note(note: NoteRequest):
    time.sleep(8) # 模拟延时
    return FAKE_NOTE_RESPONSE

@app.post("/thought", response_model=ThoughtResponse)
async def get_thought(thought: ThoughtRequest):
    return FAKE_THOUGHT_RESPONSE

@app.post("/exercise", response_model=ExerciseResponse)
async def get_exercise(exercise: ExerciseRequest):
    return FAKE_EXERCISE_RESPONSE
