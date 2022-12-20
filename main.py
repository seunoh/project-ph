from fastapi import FastAPI

from routes.v1 import api_router as v1_api_router

app = FastAPI()
app.include_router(v1_api_router, prefix='/v1')


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
