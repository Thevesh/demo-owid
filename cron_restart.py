import pandas as pd
import os

if os.path.isfile(f'done.txt'): os.remove(f'done.txt')
df = pd.DataFrame(columns=['now_at'])
df['now_at'] = [0]
df.to_csv(f'start.txt',index=False)
