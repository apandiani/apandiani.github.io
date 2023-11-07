from datetime import datetime as dt
import asyncio
import csv
from pyscript import document


async def clock():
    while True:
        now = dt.now()
        time = now.strftime("%Y-%m-%d %H:%M")
        output_div = document.querySelector("#time_output")
        output_div.innerText = time
        await asyncio.sleep(2)
run_clock = asyncio.ensure_future(clock())
