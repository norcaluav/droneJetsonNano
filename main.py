import asyncio

async def run():
    await asyncio.sleep(4)



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())