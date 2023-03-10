from MainServer.app import serve, cleanup_coroutines
import asyncio


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(serve())
    finally:
        loop.run_until_complete(*cleanup_coroutines)
        loop.close()
    asyncio.run(serve())