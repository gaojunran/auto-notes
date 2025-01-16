from typing import Union


from fastapi import FastAPI

app = FastAPI()


@app.get("/test")
def test_api():
    return {"Hello": "World"}

@app.get("/test/error")
def test_error():
    raise Exception("Test Error")

