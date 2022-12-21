from fastapi import FastAPI

from app.db.database import engine, Base
from app.routes.v1 import api_router as v1_api_router
from app.routes.short_url import router as short_url_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(v1_api_router, prefix='/v1')
app.include_router(short_url_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
