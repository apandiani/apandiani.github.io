from pyscript import document
from pyodide.http import pyfetch
# import json
# from pyodide.http import open_url
# import pandas as pd

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

# async def get_data(url):
#     response = await pyfetch(url=url, method="GET")
#     # print(await response.json())
#     data = await response.json()
#     print(data)
# server_test = asyncio.ensure_future(get_data('https://apandiani.eu.pythonanywhere.com/'))

async def show_st2():
    response = await pyfetch(url='https://apandiani.eu.pythonanywhere.com/st2', method="GET")
    data = await response.json()
    print(data)
    k_list = [k for k in data.keys()]
    st2_tot = data[k_list[0]]['Total distance']
    st2_bat = data[k_list[0]]['Battery health']
    st2_date = data[k_list[0]]['Date']
    output_tot = document.querySelector("#st2_tot")
    output_tot.innerText = f'Total distance: {st2_tot} km'
    output_bat = document.querySelector("#st2_bat")
    output_bat.innerText = f'Battery health: {st2_bat} %'
    output_date = document.querySelector("#st2_date")
    output_date.innerText = f'Last update: {st2_date}'
st2_data = asyncio.ensure_future(show_st2())


async def stromer_feed():
    response = await pyfetch(url='https://apandiani.eu.pythonanywhere.com/stromer', method="GET")
    feed = await response.json()
    print(feed)
    for x in feed:
        # print(x)
        output_div = document.querySelector("#stromer_feed")
        child = document.createElement('p')
        child.innerText = x
        output_div.appendChild(child)
        # output_div.innerText = x
        # child = document.createElement('p')
        # output_p = document.querySelector(f'#{element_id}')
stromer_feed = asyncio.ensure_future(stromer_feed())