import numpy as np
from scipy import stats as st






def dwie_srednie(dane, cecha, grupa1, grupa2, wartosc, alpha=0.05, obszar='oba'):
    '''
    

    Parameters
    ----------
    dane : TYPE pandas.DataFrame
        DESCRIPTION. Ramka danych, w której znajdują się dane
    cecha : TYPE string
        DESCRIPTION. kolumna, która opisuje przyporządkowanie do testowanych grup
    grupa1 : TYPE string
        DESCRIPTION. nazwa pierwszej grupy
    grupa2 : TYPE string
        DESCRIPTION. nazwa drugiej grupy
    wartosc : TYPE string
        DESCRIPTION. nazwa kolumny z wartociami
    alpha : TYPE float, optional
        DESCRIPTION. The default is 0.05. Poziom istotnosci.
    obszar : TYPE string, optional
        DESCRIPTION. The default is 'oba'. rodzaj hipotezy alternatywnej. Jedna wartosc z ['oba', 'lewy', 'prawy']

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    a = dane[dane[cecha] == grupa1][wartosc].array
    b = dane[dane[cecha] == grupa2][wartosc].array
    ma = np.mean(a)
    mb = np.mean(b)
    na = len(a)
    nb = len(b)
    vara = np.var(a, ddof=0)
    varb = np.var(b, ddof=0)
    u = (ma - mb) / np.sqrt(vara/na + varb/nb)
    if obszar == 'oba':
        u_alpha = st.norm.ppf(1 - alpha/2)
        p_value = (1-st.norm.cdf(abs(u)))/2
        if abs(u) >= u_alpha:
            return print('Odrzucamy hipotezę zerową na rzecz alternatywnej \n|U|={}>={}=u_alpha \nm1={}\nm2={} \np_value={}'.format(abs(u),u_alpha,ma, mb, p_value))
        if abs(u) < u_alpha:
            return print('Brak podstaw do odrzucenia hipotezy zerowej \n|U|={}<{}=u_alpha \nm1={}\nm2={} \np_value={}'.format(abs(u),u_alpha, ma, mb, p_value))
    if obszar == 'lewy':
        u_alpha = st.norm.ppf(alpha)
        p_value = st.norm.cdf(u)
        if u <= u_alpha:
            return print('Odrzucamy hipotezę zerową na rzecz alternatywnej \nU={}<={}=u_alpha \nm1={}\nm2={} \np_value={}'.format(u, u_alpha, ma, mb, p_value))
        if u > u_alpha:
            return print('Brak podstaw do odrzucenia hipotezy zerowej \nU={}>{}=u_alpha \nm1={}\nm2={} \np_value={}'.format(u,u_alpha, ma, mb, p_value))
    if obszar == 'prawy':
        u_alpha = st.norm.ppf(1 - alpha)
        p_value = 1 - st.norm.cdf(u)
        if u >= u_alpha:
            return print('Odrzucamy hipotezę zerową na rzecz alternatywnej \nU={}>={}=u_alpha \nm1={}\nm2={} \np_value={}'.format(u, u_alpha, ma, mb, p_value))
        if u < u_alpha:
            return print('Brak podstaw do odrzucenia hipotezy zerowej \nU={}<{}=u_alpha  \nm1={}\nm2={} \np_value={}'.format(u, u_alpha, ma, mb, p_value))
    return print('Test nie zadziałał, gdyż błędnie wprowadzono argumenty funkcji')

