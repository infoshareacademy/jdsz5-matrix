import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

df = pd.read_csv("../data/calendar.csv", parse_dates=['date'])

def plot_available_price(df):
    df['price'] = df['price'].str.replace('$', '')
    df['price'] = df['price'].str.replace(',', '')
    df['price'] = df['price'].astype(float)
    
    
    sns.set_style('white')
    fig, ax1 = plt.subplots(figsize=(15,6))
    ax2 = ax1.twinx()
    df_available = df.groupby('date').apply(lambda x: len(x[x['available']=='t']) / len(x)).to_frame().rename(columns={0:'available'})
    df_avgPrice = df.groupby('date').apply(lambda x: x.loc[x['available']=='t', 'price'].mean()).to_frame().rename(columns={0:'avgPrice'})
    sns.lineplot(x = df_available.index, y = 'available', ax=ax1,
                 data = df_available,color='#8C1C6C')
    sns.lineplot(x = df_avgPrice.index, y = 'avgPrice', ax=ax2,
                 data = df_avgPrice,color='#3A9B96')
    ax1.set_ylabel("udział dostępnych lokali")
    ax2.set_ylabel("średnia cena lokalu [$]")
    for tl in ax1.get_yticklabels():
        tl.set_color('#8C1C6C')
    for tl in ax2.get_yticklabels():
        tl.set_color('#3A9B96')
    ax1.yaxis.label.set_color('#8C1C6C')
    ax2.yaxis.label.set_color('#3A9B96')
    ax1.set_xlabel("data")
    sns.despine(right=False)
    plt.title("Procentowy udział lokali dostępnych i średnia cena w zakresie danego czasu")


plot_available_price(df)