import bot_telegram
import pandas as pd

from constants import TELEGRAM_GROUP_OWID

# ------------------------------------- telegram functions ------------------------------------- 
def telegram_msg(msg='', markdown=0, conf=TELEGRAM_GROUP_OWID):
    sent = 0
    while sent == 0 and conf:
        try:
            if markdown == 0:
                bot_telegram.send(messages=[msg], timeout=15, conf_custom=conf)
            else:
                bot_telegram.send(messages=[msg], timeout=15, parse_mode='markdown', conf_custom=conf)
            sent = 1
        except Exception as e:
            print(e)
            sent = 0


def telegram_image(src=None, caption=None, conf=TELEGRAM_GROUP_OWID):
    sent = 0
    while sent == 0 and conf:
        try:
            with open(src, 'rb') as f:
                bot_telegram.send(images=[f], captions=[caption], timeout=15, conf_custom=conf)
            sent = 1
        except Exception as e:
            print(e)
            sent = 0


def telegram_file(src=None, caption=None, conf=TELEGRAM_GROUP_OWID):
    sent = 0
    while sent == 0 and conf:
        try:
            with open(src, 'rb') as f:
                bot_telegram.send(files=[f], captions=[caption], timeout=15, conf_custom=conf)
            sent = 1
        except Exception as e:
            print(e)
            sent = 0


# ------------------------------------- functions to create customised date x-axis ------------------------------------- 
def keep_date(tdate, i, type):
    if type == '1m':
        return tdate.strftime('%d-%b') if i % 7 == 0 else ''
    elif type == '6m':
        return tdate.strftime('%d\n%b') if tdate.day == 1 else ''
    elif type == 'all':
        if tdate.day == 1:
            return tdate.strftime('%b\n%y') if tdate.month == 1 else tdate.strftime('%b') if tdate.month in [3, 5, 7, 9, 11] else ''
        else:
            return ''

def gen_date_xticks(date_list, type):
    ticks_dates = [pd.to_datetime(x) for x in date_list]
    ticks_dates.reverse()
    ticks_dates = [keep_date(ticks_dates[i], i, type) for i in range(len(ticks_dates))]
    ticks_dates.reverse()
    return ticks_dates
