import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import ipywidgets as widgets

from datetime import datetime

#pd.set_option('max_columns', None)

class Dataset:
    kolizje = 'Collisions.csv'
    def __str__(self):
        return 'Nasza aplikacja z kolizjami jest w trakcie budowy'

def import_data(path=Dataset.kolizje):
    print('Wyciągnięcie danych chwilę trwa, zrelaksuj się i czekaj na komunikat o zakończeniu')
    # ze względu na wielkość danych ładowanie tylko kolumn używanych do analizy
    data  = pd.read_csv(path, index_col='OBJECTID', 
                        usecols=['OBJECTID', 'X', 'Y', 'SEVERITYDESC','COLLISIONTYPE','PERSONCOUNT', 
                        'PEDCOUNT', 'PEDCYLCOUNT', 'VEHCOUNT', 'INJURIES', 'SERIOUSINJURIES', 'FATALITIES', 
                        'INCDTTM', 'SDOT_COLDESC', 'INATTENTIONIND', 'UNDERINFL', 'WEATHER', 
                        'ROADCOND', 'LIGHTCOND', 'PEDROWNOTGRNT', 'SPEEDING'])
    # zmiana nazw kolumn na bardziej intuicyjne
    data.columns = ['DLUGOSC', 'SZEROKOSC', 'DOTKLIWOSC_KOLIZJI','TYP_KOLIZJI','UCZESTNICY', 
                    'PRZECHODZIEN', 'PROWERZYSTA', 'KIEROWCA', 'RANNI', 'POWAŻNIE_RANNI', 'ŚMIERTELNIE_RANNI', 
                    'DATA', 'OPIS_ZDARZENIA', 'NIEUWAGA', 'POD_WYPLYWEM', 'POGODA', 
                    'WARUNKI_DROGOWE', 'OSWIETLENIE', 'PIERWSZENSTO_PIESZEGO', 'PRZEKORCZENIE_PREDKOSCI']
    data = cleaning_data(data)
    data = podzial_daty_na_skladowe(data)
    data = wyciągnięcie_danych_z_opisu(data)
    print('Gotowe - możesz robić analizy')

    return data
    

def cleaning_data(df):
    # wyrzucenie wierszy jeżeli uczestników zdarzenia = 0
    df.drop(df[df['UCZESTNICY'] == 0].index, inplace=True)
    # wyrzucenie danych z brakiem opisu warunków pogodowych (jest puste, albo = Unknown)
    df = df.dropna(subset=['POGODA'])
    df.drop(df[df.POGODA=='Unknown'].index, inplace=True)

    # wyrzucenie danych z brakiem opisu warunków pogodowych (jest puste, albo = Unknown)
    df = df.dropna(subset=['POGODA'])
    df.drop(df[df.POGODA=='Unknown'].index, inplace=True)

    # wyrzucenie danych z brakiem opisu kolizji
    df.drop(df[df.OPIS_ZDARZENIA=='NOT ENOUGH INFORMATION / NOT APPLICABLE'].index, inplace=True)

    # wyrzucenie danych z brakiem uczestników kolizji
    df.drop(df[df.DOTKLIWOSC_KOLIZJI=='Unknown'].index, inplace=True)

    # usunięcie przypadków, kiedy liczba rannych jest mniejsza od sumy poważnie rannych + śmiertelnych ??????????
    # sprawdź sobie przed wykonniem czyszczenia:
    # df.groupby(df['DOTKLIWOSC_KOLIZJI'])[['RANNI', 'POWAŻNIE_RANNI', 'ŚMIERTELNIE_RANNI']].sum()
    # df.drop(df[df.RANNI<(df.POWAŻNIE_RANNI+df.ŚMIERTELNIE_RANNI)].index, inplace=True)

    # standaryzacja oznaczeń w zmiennych (Y, 1, N, O, NaN) -> zamiana wartości pustych na 0, N na 0, Y na 1
    df.fillna(0, inplace=True)
    df.replace(to_replace = 'N', value = 0, inplace = True)
    df.replace(to_replace = 'Y', value = 1, inplace = True)
    # ponieważ tesktowe kolumny dalej są tekstem to trzeba je zamienic na int
    df['POD_WYPLYWEM'] = df['POD_WYPLYWEM'].astype(int)

    return df


def podzial_daty_na_skladowe(df):
    # zamiana daty ze stringa na datę i wyciągnięcie osobych kolumn: rok, miesiąc i dzień 
    # to jest najbardziej czasochłonna część przygotowania danych i to ona powoduje opóźnienie w printowaniu danych
    df['DATA'] = pd.to_datetime(df['DATA'])
    df['ROK'] = df['DATA'].dt.year
    df['MIESIAC'] = df['DATA'].dt.month
    df['DZIEN'] = df['DATA'].dt.day
    df['DZIEN_TYG'] = df['DATA'].dt.day_name()

    df['GODZINA'] = df['DATA'].dt.hour
    df['data'] = df.apply(lambda row: datetime.strptime(f"{int(row.ROK)}-{int(row.MIESIAC)}-{int(row.DZIEN)}", '%Y-%m-%d'), axis=1)

    # usunięcie zbędnej kolumny DATA
    df.drop('DATA', axis=1, inplace=True)

    return df


def wyciągnięcie_danych_z_opisu(df):
    # podział kolumny z opisem na trzy osobne kolumny ze sprawcą, poszkodowany i kierunkiem zderzenia
    # to jst drugie miejsce obciażajace czas, ale zdecydowanie mniej niż to wyżej z wyciąganiem czasu
    df.assign(SPRAWCA='', POSZKODOWANY='', KIERUNEK_SZCZEGOLY = '')

    # wyciagniecie sprawcy do osobnej kolumny
    df.loc[(df['OPIS_ZDARZENIA'].str.startswith('MOTOR'), 'SPRAWCA')] = 'POJAZD' 
    df.loc[(df['OPIS_ZDARZENIA'].str.startswith('PEDALCYCLIST'), 'SPRAWCA')] = 'ROWERZYSTA'  
    df.loc[(df['OPIS_ZDARZENIA'].str.startswith('DRIVERLESS'), 'SPRAWCA')] = 'POJAZD_BEZ_KIEROWCY'

    # wyciagniecie poszkodowanego do osobnej kolumny
    df.loc[(df['OPIS_ZDARZENIA'].str.contains('RAN OFF ROAD|STRUCK OBJECT|OVERTURNED'), 'POSZKODOWANY')] = 'BRAK' 
    df.loc[(df['OPIS_ZDARZENIA'].str.contains('STRUCK MOTOR VEHICLE'), 'POSZKODOWANY')] = 'POJAZD'  
    df.loc[(df['OPIS_ZDARZENIA'].str.contains('STRUCK PEDESTRIAN'), 'POSZKODOWANY')] = 'PRZECHODZIEN'
    df.loc[(df['OPIS_ZDARZENIA'].str.contains('STRUCK PEDALCYCLIST'), 'POSZKODOWANY')] = 'ROWERZYSTA'
    df.loc[(df['OPIS_ZDARZENIA'].str.contains('STRUCK TRAIN'), 'POSZKODOWANY')] = 'POCIAG'

    # wyciagniecie kierunku do osobnej kolumny
    df.loc[(df['OPIS_ZDARZENIA'].str.contains('FRONT'), 'KIERUNEK_SZCZEGOLY')] = 'PRZOD' 
    df.loc[(df['OPIS_ZDARZENIA'].str.contains('REAR'), 'KIERUNEK_SZCZEGOLY')] = 'TYL'  
    df.loc[(df['OPIS_ZDARZENIA'].str.contains('RIGHT'), 'KIERUNEK_SZCZEGOLY')] = 'PRAWO'
    df.loc[(df['OPIS_ZDARZENIA'].str.contains('LEFT'), 'KIERUNEK_SZCZEGOLY')] = 'LEWO'
    df['KIERUNEK_SZCZEGOLY'].fillna('BRAK', inplace=True)

    # usunięcie zbędnej kolumny OPIS_ZDARZENIA
    df.drop('OPIS_ZDARZENIA', axis=1, inplace=True)

    return df


def prognozy(df):
    df_prognozy = df.reset_index()
    df_prognozy['point'] = list(zip(df_prognozy.SZEROKOSC , df_prognozy.DLUGOSC))
    df_prognozy['tydzien'] = df_prognozy['data'].dt.strftime('%Y-%U')
    df_prognozy.drop(df_prognozy[df_prognozy['ROK'] == 2003].index, inplace = True)
    df_prognozy.drop(df_prognozy[df_prognozy['ROK'] == 2020].index, inplace = True)

    return df_prognozy


def checkbox_outlayer(pytanie):
    checkbox = widgets.Checkbox(value=False, description=pytanie, dsiabled=False, indent=False)
    return checkbox

def outlayer(wartosc, df):
    if wartosc == 0:
        # eliminacja extremnalniw odstajacąej obserwacji
        # na podstawie: df.groupby(df['TYP_KOLIZJI'])[['RANNI']].max()
        #df = df.drop(df[df.RANNI==78].index)
        df = df.loc[df['RANNI'] != 78]
        print('Wybrałeś analizę na danych BEZ obserwacji odstających')
    else:
        df = df
        print('Wybrałeś analizę na danych Z obserwacjami odstającymi')
    return df

def wybor_lat(pytanie):
    lata = widgets.IntRangeSlider(value=[2004, 2020], min=2004, max=2020, step=1, description=pytanie)
    return lata

def zakres_lat(lata, df):
    rok_min = min(lata)
    rok_max = max(lata)
    df = df.loc[(df['ROK'] > rok_min) & (df['ROK'] <= rok_max)]
    print(f'Wybrałeś lata pomiędzy {rok_min}, a {rok_max}')
    return df
    
def rysuj_boxplot(df, x, y):
    plt.figure(figsize=(20,10))  # rozszerzenie wykresu na całą stronę
    sns.boxplot(data=df, x=x, y=y, orient="h")  # rysowanie wykresu skrzykowego
    