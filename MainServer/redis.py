from redis.asyncio import Redis
from .settings import settings


async_session = Redis(host=settings.redis_host,
                      port=settings.redis_port,
                      db=0,
                      username=settings.redis_user,
                      password=settings.redis_user_password,
                      decode_responses=True,
                      encoding="utf-8")


async def get_session() -> Redis:
    async with async_session.client() as session:
        try:
            yield session
        finally:
            await session.close()
