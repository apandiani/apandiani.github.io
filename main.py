from datetime import datetime as dt
import asyncio
import csv


async def clock():
    while True:
        now = dt.now()
        time = now.strftime("%Y-%m-%d %H:%M")
        # print(time)
        Element("time_output").write(time)
        await asyncio.sleep(2)
run_clock = asyncio.ensure_future(clock())


# def get_timestamp():
#     timestamp_csv = 'timestamp.csv'
#     with open(timestamp_csv) as csvfile:
#         reader = csv.reader(csvfile)
#         time_list = [row for row in reader]
#         last_log = time_list[-1][0]
#         time_date = last_log[:-6]
#         Element("logged_time").write(time_date)
#         # print(time_date)
# timestamp = get_timestamp()

