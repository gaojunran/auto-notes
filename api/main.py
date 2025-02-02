from pathlib import Path
import time

from api.functions.export import generate_note
from api.models import (
    ExportRequest,
    NetworkRequest,
    NetworkResponse,
    NoteRequest,
    NoteResponse,
    RecordResponse,
)
from fastapi import FastAPI, UploadFile

CWD = Path.cwd()

app = FastAPI()


@app.get("/test")
async def test(fake: bool = False):
    return {"response": "OK"}


@app.post("/record", response_model=RecordResponse)
async def post_record(file: UploadFile, fake: bool = False):
    print(file, fake)
    if fake:
        time.sleep(2)  # 模拟延时
        return RecordResponse.fake()
    raise NotImplementedError()  # TODO


@app.post("/note", response_model=NoteResponse)
async def get_note(note: NoteRequest, fake: bool = False):
    if fake:
        time.sleep(2)  # 模拟延时
        return NoteResponse.fake()
    raise NotImplementedError()  # TODO


@app.post("/network", response_model=NetworkResponse)
async def get_network(network: NetworkRequest, fake: bool = False):
    if fake:
        time.sleep(2)  # 模拟延时
        return NetworkResponse.fake()
    raise NotImplementedError()  # TODO


@app.post("/export")
async def export(content: ExportRequest, fake: bool = False):
    json_string = content.model_dump_json()
    with open(CWD / "typst" / "content.json", "w", encoding="utf-8") as f:
        f.write(json_string)
    generate_note(content.topic)
    return {"response": "OK"}
