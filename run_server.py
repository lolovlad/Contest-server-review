from MainServer.app import serve, cleanup_coroutines
import asyncio


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(serve())
finally:
    try:
        loop.run_until_complete(*cleanup_coroutines)
        loop.close()
    except TypeError:
        loop.close()
asyncio.run(serve())