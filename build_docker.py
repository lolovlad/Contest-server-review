import docker
import aiodocker
import asyncio
import redis.asyncio as redis
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    server_host: str
    server_port: int
    static_path: str

    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_db: str
    postgres_password: str
    pgport: int

    redis_password: str
    redis_user: str
    redis_user_password: str

    redis_host: str
    redis_port: int

    minio_access_key: str
    minio_secret_key: str
    minio_default_buckets: str
    minio_host: str
    minio_port: str

    minio_root_user: str
    minio_root_password: str

    websocket_server_host: str
    websocket_server_port: int


settings = Settings(_env_file="settings_server_debug.env", _env_file_encoding="utf-8")

count_docker = 1


def create_image():
    client = docker.from_env()
    try:
        client.images.get("review_app")
    except:
        client.images.build(
            path="../Cheacker/",
            tag="review_app"
        )


async def start_container():
    aio_client = aiodocker.Docker()
    r = redis.Redis(host=settings.redis_host,
                    port=settings.redis_port,
                    db=0,
                    username=settings.redis_user,
                    password=settings.redis_user_password,
                    decode_responses=True)
    async with r.client() as conn:
        for i in range(count_docker):
            container = await aio_client.containers.create_or_replace(
                config={
                    'Image': 'review_app',
                    'Cmd': ["python3", "/app/main.py"],
                    "AttachStdin": True,
                    "AttachStdout": True,
                    "AttachStderr": True,
                    "Tty": False,
                    "OpenStdin": True,
                    "StdinOnce": True,
                },
                name=f"review-app-{i}"
            )
            await container.start()
            await conn.set(container.id, "free")


async def main():
    create_image()
    await start_container()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
