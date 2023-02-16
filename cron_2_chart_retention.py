import pandas as pd
import numpy as np
import seaborn as sb
import traceback
import matplotlib.pyplot as plt

from constants import GCS_RETENTION

def chart_retention():
    res = {'status': 0, 'message': f'🔄 Process exited, but without error?'}

    try:
        col_index = ['donor_id','visit_date']

        # retention analysis function - avoids duplication, easy to scale for other permutations
        def retention_analysis(f1=None, f2=None):
            f1 = pd.merge(f1, f2, on='donor_id',how='left').drop('donor_id',axis=1)
            f1 = f1.groupby('visit_date').sum().reset_index()

            res = pd.DataFrame(columns=[x for x in range(len(f1.columns)-1)])
            first_year, last_year = f1.columns[1], f1.columns[-1]
            for c in f1.columns[1:]:
                res.loc[c] = list(f1[f1.visit_date == c][list(range(c,last_year+1))].iloc[0]) + [np.nan]*(c-first_year)
            for c in res.columns[1:]: res[c] = res[c]/res[0] * 100
            res[0] = 100 

            return res

        # base frame, analysis conducted on an annual basis
        df = pd.read_parquet(GCS_RETENTION, columns=col_index)
        df['visit_date'] = pd.to_datetime(df.visit_date).dt.year

        # rf is the "regular" frame, defined here as >2x per year; ymmv
        rf = df.groupby(col_index).size().to_frame('n_donations').reset_index()\
            .loc[lambda x: x['n_donations'] > 2].drop('n_donations',axis=1)
        
        # hf is the "hardcore" frame, defined here as >5x per year; ymmv
        hf = df.groupby(col_index).size().to_frame('n_donations').reset_index()\
            .loc[lambda x: x['n_donations'] > 5].drop('n_donations',axis=1)

        # after creating rf, drop duplicates from df to get base frame
        df = df.drop_duplicates(subset=['donor_id','visit_date']).reset_index(drop=True)

        # pf is the "pivoted" frame; can be left-joined onto df, rf, and any other frames of similar type
        pf = df.assign(donated=1).pivot(index='donor_id',columns='visit_date',values='donated').reset_index()

        # call retention function
        df = retention_analysis(f1=df, f2=pf)
        rf = retention_analysis(f1=rf, f2=pf)
        # hf = retention_analysis(f1=hf, f2=pf)

        # plot charts
        toggles = {
            'df': [df,rf,hf],
            'label': ['1x','3x','6x'],
            'cmap': ['Blues','Purples','magma'],
            'output': ['total','regular','hardcore']
        }

        for plot in [0,1]:
            fig, ax = plt.subplots(figsize=(8,6))
            fontsize = 10
            sb.set(font="Monospace")

            sb.heatmap(toggles['df'][plot],
                    annot=True, fmt=".0f",
                    annot_kws={'font': 'Monospace', 'fontsize': fontsize},
                    cmap=toggles['cmap'][plot],
                    vmin=0, vmax=toggles['df'][plot][1].max()+10,
                    cbar = False,
                    cbar_kws={"shrink": .9}, ax=ax)
            ax.set_ylabel(f'Donated Blood At Least {toggles["label"][plot]} in\n')
            ax.set_xlabel('')
            ax.set_facecolor('white')
            plt.yticks(rotation=0)
            plt.tick_params(axis='both', which='major', labelsize=fontsize, 
                            labelbottom = False, labeltop=True, left=False, bottom=False, top = False)
            ax.set_title('% of Donors Still Donating after N Years\n')
            plt.text(9,11, f"""
            Sample Interpretation:\n
            Thus far, {toggles['df'][plot].iloc[-2,1]:.0f}% of those who
            donated at least {toggles['label'][plot].lower()} in {toggles['df'][plot].index[-2]}
            have made a donation
            in {toggles['df'][plot].index[-1]}.
            """, horizontalalignment='center', color='grey') # Add sample inerpretation
            plt.savefig(f'charts/chart_retention_{toggles["output"][plot]}.png', bbox_inches="tight", dpi=400)
            plt.close()

        res['status'] = 1
        res['message'] = f'✅ Retention charts produced'
    except Exception as e:
        res['message'] = f'❌ Error while producing retention charts:\n\n{traceback.format_exc()}'
    
    return res

# print(chart_retention()) # if you need to test it modularly