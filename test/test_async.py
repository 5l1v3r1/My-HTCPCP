import asyncio
import sys
import aiohttp

session = None
async def a():
    global session
    session = aiohttp.ClientSession()
    for i in range(3):
        await asyncio.sleep(1)
        print(1)
    await session.close()
    sys.exit(0)

async def b():
    while True:
        await asyncio.sleep(1)
        await session.request("get", "https://www.baidu.com/")
        print(2)

async def main():
    asyncio.create_task(a())
    asyncio.create_task(b())
    await asyncio.sleep(100)

asyncio.run(main())