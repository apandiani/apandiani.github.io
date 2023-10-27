from datetime import datetime as dt
import asyncio
# import csv


async def clock():
    while True:
        now = dt.now()
        time = now.strftime("%Y-%m-%d %H:%M")
        # print(time)
        Element("time_output").write(time)
        await asyncio.sleep(2)
run_clock = asyncio.ensure_future(clock())
