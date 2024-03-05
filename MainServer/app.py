from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, func

from .Api import router
from .settings import settings


origins = [
    f"http://localhost"
]

app = FastAPI()

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


'''cleanup_coroutines = []


async def serve():
    server = aio.server()

    #file_pb2_grpc.add_FileApiServicer_to_server(FileProtoService(), server)

    server.add_insecure_port(f'{settings.server_host}:{settings.server_port}')
    print("start_server")
    await server.start()

    async def server_graceful_shutdown():
        await server.stop(5)

    cleanup_coroutines.append(server_graceful_shutdown())
    await server.wait_for_termination()'''