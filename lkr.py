from pyscript import document, display, when
from pyodide.http import pyfetch
from pyodide.ffi import create_proxy

import matplotlib.pyplot as plt
import io
import base64

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
await show_lkr()


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