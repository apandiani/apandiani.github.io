from pyscript import document, display, when
from pyodide.http import pyfetch
from pyodide.ffi import create_proxy
from js import document

import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime as dt
import asyncio

async def clock():
    while True:
        now = dt.now()
        time = now.strftime("%d.%m.%Y %H:%M")
        # display(time, target='#time_output')
        output_div = document.querySelector("#time_output")
        output_div.innerText = time
        await asyncio.sleep(2)
run_clock = asyncio.ensure_future(clock())


def format_time(v):
    t = dt.fromtimestamp(v)
    # tz_bub = pytz.timezone(TZ_BUB)
    # tz_hyd = pytz.timezone(TZ_HYD)
    # t = tz_bub.localize(t)
    # if z == 'hyderabad':
        # t = t.astimezone(tz_hyd)
    t = t.strftime('%H:%M')
    return t

async def show_owm():
    lat = 47.25659196257891
    lon = 8.854448486942953
    api_key = '1de97342bb9f3b6c38127ff0d7b979bd'
    # url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}&units=metric'
    response = await pyfetch(url=f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}&units=metric', method="GET")
    data = await response.json()
    # print(data)

    update_time = data['current']['dt']
    display(f'Last update: {format_time(update_time)}', target='owm_date', append=False)

    current_temp = data['current']['temp']
    current_sunrise = data['current']['sunrise']
    current_sunset = data['current']['sunset']
    current_weather = data['current']['weather'][0]['description']

    current_list = [current_temp, current_sunrise, current_sunset, current_weather]
    for i in current_list:
        display(i, target='owm', append=True)

    # sender = type(data['alerts'])
    # print(sender)
    # for i in sender:
        # display(i, target='owm', append=True)

owp_data = asyncio.ensure_future(show_owm())


async def show_st2():
    response = await pyfetch(url='https://apandiani.eu.pythonanywhere.com/st2', method="GET")
    data = await response.json()
    # print(data)
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
    # print(feed)
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
    last_entry = data[-1]
    # print(last_entry)
    lkr = last_entry['LKR']
    lkr = float(lkr)
    lkr_date = last_entry['Date']
    output_lkr = document.querySelector("#lkr")
    output_lkr.innerText = f'{int(lkr)} LKR'
    output_lkr_date = document.querySelector("#lkr_date")
    output_lkr_date.innerText = f'Last update: {lkr_date}'

    dat_list = [d['Date'] for d in data[-30:]]
    lkr_list = [float(l['LKR']) for l in data[-30:]]
    # print(lkr_list)
    fig, ax = plt.subplots(facecolor="#373737")

    plt.setp(ax.spines.values(), color='white')
    plt.setp([ax.get_xticklines(), ax.get_yticklines()], color='white')
    plt.tight_layout()
    
    ax.plot(dat_list, lkr_list, color='orange')
    ax.set_facecolor(color="#373737")
    ax.set_ylabel(ylabel='', color="white")
    ax.tick_params(labelcolor='white')
    ax.tick_params(axis='y', colors='white')
    ax.get_xaxis().set_visible(False)

    # display(fig, target="lkr_plot")
    
    img = io.BytesIO()
    fig.savefig(img, format='png',
                bbox_inches='tight')
    img.seek(0)
    encoded = base64.b64encode(img.getvalue())
    output_plot = document.querySelector("#lkr_plot")
    output_plot.src = "data:image/png;base64, {}".format(encoded.decode('utf-8'))
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

@when("click", "#lkr_reset")
def reset_lkr(event):
    chf = document.querySelector("#input_chf")
    chf.value = None
    lkr = document.querySelector("#input_lkr")
    lkr.value = None