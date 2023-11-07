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
# import pyodide_http
# pyodide_http.patch_all()
# import requests
# import pandas as pd
# import io

async def csv(file):
	# username = os.environ['csv_username']
	# token = os.environ['csv_token']
    username = 'apandiani'
    token = '259fd04469ea337c8c32be28183b84536e59c7ba'
 
    path = '/home/apandiani/requests/{file}.csv'.format(file=file)

    URL = 'https://eu.pythonanywhere.com/api/v0/user/{username}/files/path{path}'.format(username=username, path=path)
    response = await pyfetch(url=URL, method="GET")
    

    # response = await requests.get(
	#  'https://eu.pythonanywhere.com/api/v0/user/{username}/files/path{path}'.
	#  format(username=username, path=path),
	#  headers={'Authorization': 'Token {token}'.format(token=token)})

    print(response.status)

    # df = pd.read_csv(io.StringIO(response.content.decode('utf_8')))

    # return df
# st2 = asyncio.ensure_future(csv('get_st2'))
