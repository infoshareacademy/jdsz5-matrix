import pandas as pd
import numpy as np
import math
import random
from scipy.stats import ttest_ind
from scipy.stats import poisson

import folium                                                                   
from folium import plugins
import plotly.express as px

def srednia_miesiac(df_prognozy):
    monthly = df_prognozy.groupby(['data','MIESIAC']).count()['OBJECTID'].reset_index()
    monthly = monthly.groupby('MIESIAC').mean()

    return monthly

def testSrednich_bootstrap(df_prognozy, nr_miesiacaA, nr_miesiacaB, n=1000,alpha=0.05):
    monthly = df_prognozy.groupby(['data','MIESIAC']).count()['OBJECTID'].reset_index()
    monthly.groupby('MIESIAC').mean()
    x = np.array(monthly.loc[monthly['MIESIAC'] == nr_miesiacaA ]['OBJECTID'])
    y = np.array(monthly.loc[monthly['MIESIAC'] == nr_miesiacaB ]['OBJECTID'])
    pvalue = ttest_ind(x,y).pvalue
    print("p-value={:.4} jest {} niż poziom istotności {}.".format(pvalue,"większa" if pvalue>alpha else "mniejsza", alpha))
    if pvalue>alpha:
        print("Brak podstaw do odrzucenia hipotezy zerowej: średnie są równe.")
    else:
        print("Hipotezę zerową należy odrzucić na rzecz hipotezy alternatywnej: średnie nie są równe.")

    pvalues= []
    for i in range(n):
        sample_x = np.random.choice(x,len(x),replace=True)
        sample_y = np.random.choice(y,len(y),replace=True)
        tst = ttest_ind(sample_x,sample_y)
        p = (tst.pvalue < alpha)*1
        pvalues.append(p)
        
    print('Wynik testu istotny w {0} symulacji.'.format(  "{:.1%}".format(np.mean(pvalues) )))


def bootstrap_przedzial_roznicy(df_prognozy, nr_miesiacaA, nr_miesiacaB, n=1000,alpha=0.05):                                              
    monthly = df_prognozy.groupby(['data','MIESIAC']).count()['OBJECTID'].reset_index()
    monthly.groupby('MIESIAC').mean()
    x = np.array(monthly.loc[monthly['MIESIAC'] == nr_miesiacaA ]['OBJECTID'])
    y = np.array(monthly.loc[monthly['MIESIAC'] == nr_miesiacaB ]['OBJECTID'])
    diff = []
    for i in range(n):
        # losujemy e zwracaniem i liczymy różnicę
        sample_x = np.random.choice(x,len(x),replace=True)
        sample_y = np.random.choice(y,len(y),replace=True)
        diff.append(np.mean(sample_x)-np.mean(sample_y))
    #wyliczamy przedział ufności dla róznic
    orig_diff = np.mean(x) - np.mean(y)
    # przedział dolny 
    lcb =  orig_diff + np.percentile(diff,alpha/2)
    # przedział górny 
    ucb =  orig_diff + np.percentile(diff,1-alpha/2)
    include_zero = lcb < 0 and ucb >0 
    if include_zero:
        info = '0 zawiera się w przedziale ufności, więc nie mamy podstaw twierdzić że róznica jest istotna.'
    else:
        info = '0 nie zawiera się w przedziale ufności, więc przyjmujemy różnicę za istotną.'
    
    print('Przedział ufności różnic: ({0},{1})'.format(lcb.round(4),ucb.round(4)))
    print(info)


def prawdopodobienstwo(k, mu):
    prawdopA = poisson.pmf(k, mu)
    print('W następnym tygodniu nie będzie kolizji: {}'.format(prawdopA))

    #prawdopB = poisson.pmf(k+2, mu)
    #print('Będą dokładnie 2 kolizje w następnym tygodniu: {}'.format(prawdopB))

    prawdopC = poisson.pmf(k, mu) + poisson.pmf(k+1, mu) + poisson.pmf(k+2, mu)
    print('Będą maksymalnie 2 kolizje w następnym tygodniu: {}'.format(prawdopC))

    #prawdopD = 1 - (poisson.pmf(k, mu*2) + poisson.pmf(k+1, mu*2))
    #print('Prawdopodobieńśtwo, że w ciągu następnych 2 tygodni będą przynajmniej 2 kolizje: {}'.format(prawdopD))


def top_miejsc_kolizji(tab):
    
    mapa = folium.Map(location=[47.607612, -122.333515], zoom_start=10)

    #px.set_mapbox_access_token(open(".mapbox_token").read())
    col = tab
    fig = px.scatter_mapbox(col, lat="SZEROKOSC", lon="DLUGOSC",     color="Ilosc kol.", size="Ilosc kol.",
                      color_continuous_scale=px.colors.sequential.matter, size_max=30, zoom=10)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


    print('Lokalizacja 100 miejsc z największą ilością kolizji')
    fig.show()