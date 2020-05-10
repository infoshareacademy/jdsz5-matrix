import pandas as pd
import numpy as np
import math
import random
from scipy.stats import ttest_ind
from scipy.stats import poisson

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

def prawdopodobienstwo(k, mu):
    prawdopA = poisson.pmf(k, mu)
    print('Prawdopodpbieństwo, że w następnym tygodniu nie będzie kolizji w danym miejscu: {}'.format(prawdopA))

    prawdopB = poisson.pmf(k+2, mu)
    print('Prawdopodobieństwo, że będą dokładnie 2 kolizje w następnym tygodniu: {}'.format(prawdopB))

    prawdopC = poisson.pmf(k, mu) + poisson.pmf(k+1, mu) + poisson.pmf(k+2, mu)
    print('Prawdopodobieństwo, że będą maksymalnie 2 kolizje w następnym tygodniu: {}'.format(prawdopC))

    prawdopD = 1 - (poisson.pmf(k, mu*2) + poisson.pmf(k+1, mu*2))
    print('Prawdopodobieńśtwo, że w ciągu następnych 2 tygodni będą przynajmniej 2 kolizje: {}'.format(prawdopD))