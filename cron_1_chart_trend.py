import pandas as pd
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

from helper import gen_date_xticks
from constants import GITHUB_DONATIONS

def chart_trends(target=None):
    res = {'status': 0, 'message': f'🔄 Process exited, but without error?'}

    try:
        plot_column = 'daily'
        df = pd.read_csv(GITHUB_DONATIONS, usecols=['date','state','daily'], parse_dates=['date'])
        df = df[(df.state == 'Malaysia') & (df.date.dt.date >= target-relativedelta(years=2))][['date','daily']]
        df[f'{plot_column}_7d'] = df[plot_column].rolling(7).mean()

        date_mid = target - relativedelta(months=6)
        date_short = target - relativedelta(months=1)

        df_views = {
            0: df.copy(),
            1: df.tail((target-date_mid).days+1),
            2: df.tail((target-date_short).days+1)
        }
        df_views_xticks = {
            0: gen_date_xticks(df_views[0].date.tolist(), 'all'),
            1: gen_date_xticks(df_views[1].date.tolist(), '6m'),
            2: gen_date_xticks(df_views[2].date.tolist(), '1m'),
        }

        plt.rcParams.update({'font.size': 11,
                            'font.family': 'sans-serif',
                            'grid.linestyle': 'dashed',
                            'figure.figsize': [7, 14],
                            'figure.autolayout': True})
        fig, ax = plt.subplots(3, 1)
        axes = ax.ravel()

        for i in range(3):
            dfp = df_views[i].reset_index(drop=True)
            dfp.date = pd.to_datetime(dfp.date)
            plot_range = f'{dfp.date.iloc[0]:%d-%b-%Y} to {dfp.date.iloc[-1]:%d-%b-%Y}'

            dfp[plot_column].plot(kind='bar', color='lightgrey', ax=axes[i])
            dfp[f'{plot_column}_7d'].plot(kind='line', marker=None, color='red', ax=axes[i])
            axes[i].yaxis.grid(True)
            axes[i].yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # comma-sep y-axis
            axes[i].set(xticklabels=df_views_xticks[i]) # custom x-axis labels
            axes[i].tick_params(axis='both', which='both', length=0) # remove ticks but keep labels
            axes[i].set_title(f'\n{plot_range}\n')

        plt.suptitle('Malaysia: Daily Blood Donations')
        plt.savefig(f'charts/chart_trends.png', pad_inches=0.2, dpi=400)

        res['status'] = 1
        res['message'] = f'✅ Trend chart produced'
    except Exception as e:
        res['message'] = f'❌ Error while producing trend chart:\n\n{e}'
    
    return res

# print(chart_trends(target=date.today()-timedelta(1))) # if you need to test it modularly