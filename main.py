from pyscript import document
from pyodide.http import pyfetch
from pyodide.ffi import create_proxy
from js import document

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
    st2_tot = data['Total distance']
    st2_tot = int(float(st2_tot))
    st2_bat = data['Battery health']
    st2_date = data['Date']
    output_tot = document.querySelector("#st2_tot")
    output_tot.innerText = f'{st2_tot} km'
    output_bat = document.querySelector("#st2_bat")
    output_bat.innerText = f'{st2_bat} %'
    output_date = document.querySelector("#st2_date")
    output_date.innerText = f'Last update: {st2_date}'
st2_data = asyncio.ensure_future(show_st2())


async def stromer_feed():
    response = await pyfetch(url='https://apandiani.eu.pythonanywhere.com/stromer', method="GET")
    feed = await response.json()
    print(feed)
    for x in feed:
        output_div = document.querySelector("#stromer_feed")
        child = document.createElement('p')
        child.innerText = x
        output_div.appendChild(child)
stromer_feed = asyncio.ensure_future(stromer_feed())


async def show_lkr():
    global lkr
    response = await pyfetch(url='https://apandiani.eu.pythonanywhere.com/lkr', method="GET")
    data = await response.json()
    print(data)
    lkr = data['LKR']
    lkr = round(float(lkr), 1)
    lkr_date = data['Date']
    output_lkr = document.querySelector("#lkr")
    output_lkr.innerText = f'{lkr} LKR'
    output_lkr_date = document.querySelector("#lkr_date")
    output_lkr_date.innerText = f'Last update: {lkr_date}'
lkr_data = asyncio.ensure_future(show_lkr())


write_in_progress = False

def isTemp(input_temp):
    try:
        _ = float(input_temp)
    except Exception as err:
        return False
    
    return True

def _c(self, *args, **kwargs):
    global write_in_progress
    if write_in_progress:
        return
    else:
        write_in_progress = True
        c_input = document.getElementById("input_chf")
        l_output = document.getElementById("input_lkr")
        input_value = c_input.value
        if isTemp(input_value):
            l_output.value = round((int(float(input_value)) * lkr))
        else:
            l_output.value = ""
        write_in_progress = False

def _l(self, *args, **kwargs):
    global write_in_progress
    if write_in_progress:
        return
    else:
        write_in_progress = True
        l_input = document.getElementById("input_lkr")
        c_output = document.getElementById("input_chf")
        input_value = l_input.value
        if isTemp(input_value):
            c_output.value = round((int(float(input_value))) / lkr)
        else:
            c_output.value = ""
        write_in_progress = False

c_change = create_proxy(_c)
l_change = create_proxy(_l)

document.querySelector("#input_chf").addEventListener("input", c_change)
document.querySelector("#input_lkr").addEventListener("input", l_change)

def reset_lkr(event):
    chf = document.querySelector("#input_chf")
    chf.value = None
    lkr = document.querySelector("#input_lkr")
    lkr.value = None