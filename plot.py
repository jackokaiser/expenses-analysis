import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy import stats


def get_end_time(csv_path):
    end_sec = int(os.path.splitext(os.path.basename(csv_path))[0])
    return pd.to_datetime(end_sec, unit='s')


if __name__ == "__main__":
    csv_path = os.path.join('data', 'Splitwise export for Couple.csv')
    df = pd.read_csv(csv_path)
    df.replace(' ', float('NaN'), inplace=True)
    df.dropna(subset=["Cost"], inplace=True)
    df['Cost'] = pd.to_numeric(df['Cost'])
    df['Date'] = pd.to_datetime(df['Date'])

    from_date = '2021-06-01'
    to_date = df['Date'].iloc[-1].date()
    df = df[df['Date'] >= '2021-06-01']

    categories = df.groupby(['Category']).sum()
    categories.sort_values('Cost', ascending=False, inplace=True)
    total_cost = categories["Cost"].sum()
    print(categories)
    print(f'total cost: {total_cost}€')

    legend_loc = {'loc': 'center left', 'bbox_to_anchor': (1.0, 0.5)}
    height = 7
    fig, axs = plt.subplots(1, 2, figsize=[1.618 * height, height])
    fig.suptitle(f'Expenses from {from_date} to {to_date} (total {total_cost}€)', fontsize=16)

    cost_series = categories[(categories['Cost'] / total_cost) >= 0.01]['Cost']
    cost_series.plot.pie(y='Cost', ax=axs[0], legend=False)
    cost_series.plot.bar(y='Cost', ax=axs[1], rot=60)
    plt.tight_layout()

    fig.savefig('expenses.png')
