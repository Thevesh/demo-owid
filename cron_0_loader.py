import pandas as pd
from datetime import date, timedelta
from constants import GITHUB_DONATIONS

# function to check if latest data is in
def check_latest_data(target=None):
    res = {'status': 0, 'message': f'🔄 File okay, but data for {target.strftime("%d-%b")} is not in'}
    try:
        df = pd.read_csv(GITHUB_DONATIONS,usecols=['date'])
        latest_date = pd.to_datetime(df['date']).dt.date.max()

        if latest_date == target:
            res['status'] = 1
            res['message'] = f'✅ Data for {target.strftime("%d-%b")} is in!'
    except Exception as e:
        res['message'] = f'❌ Error while checking donations CSV:\n\n{e}'

    return res

# check_latest_data(target=date.today()-timedelta(1)) # if you need to test it modularly