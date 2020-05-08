import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def kolizje_miesiac(df_prognozy):
    sns.set_style('white')
    fig, ax = plt.subplots(figsize=(15,6))

    df_prognozy.set_index('data').resample('M').size().plot(label='Ilość kolizji na miesiąc', color='grey', ax=ax)
    df_prognozy.set_index('data').resample('M').size().rolling(window=12).mean().plot(color='blue', linewidth=5, label='Średnia roczna ilość kolizji', ax=ax)

    ax.set_title('Ilość kolizji na miesiąc', fontsize=14, fontweight='bold')
    ax.set(ylabel='Ilość kolizji\n', xlabel='')
    ax.legend(bbox_to_anchor=(1.1, 1.1), frameon=False)
    sns.despine(ax=ax, top=True, right=True, left=True, bottom=False)

def kolizje_rok_dzien(df_prognozy):
    nazwa_dzien = ['Sunday', 'Saturday', 'Friday', 'Thursday', 'Wednesday', 'Tuesday', 'Monday']
    dzien_tyg = df_prognozy['data'].dt.weekday_name
    rok = df_prognozy['data'].dt.year

    tabela_kolizje = df_prognozy.groupby([rok, dzien_tyg]).size()
    tabela_kolizje = tabela_kolizje.rename_axis(['rok', 'dzien_tyg']).unstack('dzien_tyg').reindex(columns=nazwa_dzien)
    
    plt.figure(figsize=(10,7))
    sns.heatmap(tabela_kolizje, cmap='Blues')
    plt.title('\nKolizje w danym roku i dniu tygodnia\n', fontsize=14, fontweight='bold')
    plt.xlabel('')
    plt.ylabel('')

def kolizje_doba(df_prognozy):
    sns.set_style('white')
    fig, ax = plt.subplots(figsize=(10,6))

    df_prognozy.GODZINA.hist(range=(1,25), bins=24, ax=ax, color='lightblue')
    ax.set_title('\n Rokład kolizji w ciągu doby\n', fontsize=14, fontweight='bold')
    ax.set(xlabel='Godzina', ylabel='Ilość kolizji')
    sns.despine(top=True, right=True, left=True, bottom=True)