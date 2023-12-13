from pyscript import document, display
from pyodide.http import pyfetch

from datetime import datetime as dt

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
    current_day = data['daily'][0]['summary']

    current_list = [current_temp, current_sunrise, current_sunset, current_weather, 
                    current_day]
    for i in current_list:
        display(i, target='owm', append=True)

    # sender = type(data['alerts'])
    # print(sender)
    # for i in sender:
        # display(i, target='owm', append=True)

await show_owm()
