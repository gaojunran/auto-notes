import time

from api.models import (
    NetworkRequest,
    NetworkResponse,
    NoteRequest,
    NoteResponse,
    RecordResponse,
)
from fastapi import FastAPI, UploadFile

app = FastAPI()


@app.get("/test")
async def test(fake: bool = False):
    return {"response": "OK"}


@app.post("/record", response_model=RecordResponse)
async def post_record(file: UploadFile, fake: bool = False):
    if fake:
        time.sleep(2)  # 模拟延时
        return RecordResponse.fake()
    ...      # TODO


@app.post("/note", response_model=NoteResponse)
async def get_note(note: NoteRequest, fake: bool = False):
    if fake:
        time.sleep(2)  # 模拟延时
        return NoteResponse.fake()
    ...      # TODO


@app.post("/network", response_model=NetworkResponse)
async def get_network(network: NetworkRequest, fake: bool = False):
    if fake:
        time.sleep(2)  # 模拟延时
        return NetworkResponse.fake()
    ...      # TODO
