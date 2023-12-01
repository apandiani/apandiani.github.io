from pyscript import document

from datetime import datetime as dt
import asyncio

async def clock():
    while True:
        await asyncio.sleep(2)
        now = dt.now()
        time = now.strftime("%d.%m.%Y %H:%M")
        # display(time, target='#time_output')
        output_div = document.querySelector("#time_output")
        output_div.innerText = time
        
await clock()