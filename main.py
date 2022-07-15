from functions.core import open_spot, open_futures
import asyncio

SYMBOL_QNT = {
    'AVAXUSDT': 1,
}

async def main():
    tasks = []
    for key in SYMBOL_QNT:
        tasks.append(asyncio.create_task(open_spot(key, SYMBOL_QNT[key])))
        tasks.append(asyncio.create_task(open_futures(key, SYMBOL_QNT[key])))

    await asyncio.gather(*tasks)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
