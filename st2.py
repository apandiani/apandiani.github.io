from pyscript import document
from pyodide.http import pyfetch

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
await show_st2()


async def stromer_feed():
    response = await pyfetch(url='https://apandiani.eu.pythonanywhere.com/stromer', method="GET")
    feed = await response.json()
    # print(feed)
    for x in feed:
        output_div = document.querySelector("#stromer_feed")
        child = document.createElement('p')
        child.innerText = x
        output_div.appendChild(child)
await stromer_feed()