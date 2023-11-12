from pyscript import document

from datetime import datetime as dt
import asyncio


async def clock():
    while True:
        now = dt.now()
        time = now.strftime("%d.%m.%Y %H:%M")
        output_div = document.querySelector("#time_output")
        output_div.innerText = time
        await asyncio.sleep(2)
run_clock = asyncio.ensure_future(clock())


# from pyodide.http import pyfetch
# import pandas as pd

# async def csv(file):
 

    
    # response = await pyfetch(url=file, method="GET")
    

    # print(response.status)

    # df = pd.read_csv(response)
    # print(df)
    # return df

# URL = 'https://apandiani.eu.pythonanywhere.com/csv/get_st2.csv'
# st2 = asyncio.ensure_future(csv(URL))
