from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, func

from .Api import router
from .settings import settings
import asyncio

from MainServer.Services.ReviewDockerServices import ReviewDockerServices


origins = [
    f"http://localhost"
]


async def load_redis_message():
    service = ReviewDockerServices()
    while True:
        message = await service.get_message_in_redis()
        print(message.trace_uuid, message.points, "total review")
        await service.save_result_in_db(message)


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(load_redis_message())
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Count-Page", "X-Count-Item"],
)

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello World"}