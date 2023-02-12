import os
if os.path.isfile(f'done.txt'): exit()

import pandas as pd
from datetime import date, timedelta

from helper import telegram_msg, telegram_image

from cron_0_loader import check_latest_data
from cron_1_chart_trend import chart_trends


# simple function to call the right step
def call_function(x, target=None):
    res = {'status': 0, 'message': ''}

    if x == 0: return check_latest_data(target=target)
    elif x  == 1: return chart_trends(target=target)

    return res


# tracker to enable modularised cron job + pick-up where left
tracker = pd.read_csv(f'start.txt')
current_step = tracker['now_at'].iloc[0]
tdate = date.today() - timedelta(2)


# run from where we left, as far as possible
MAX_STEPS = 2
if current_step < MAX_STEPS:
    for i in range(current_step, MAX_STEPS):
        res = call_function(i)
        telegram_msg(msg=res['message'])
        if res['status'] == 1:
            tracker['now_at'] = [i + 1]
            tracker.to_csv(f'start.txt',index=False)
        else: exit() # exit at this step if not completed

# when everything is completed, send surveillance output
for s in ['trends']: telegram_image(src=f'chart_{s}.png', caption=f'Update ({s}): {tdate:%Y-%m-%d}')