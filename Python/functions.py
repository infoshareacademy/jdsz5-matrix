import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import ipywidgets as widgets
import warnings
from ipywidgets import HBox, VBox

import math                                        
import random                                      
from scipy.stats import ttest_ind                  
from datetime import datetime                      

class Dataset:
    kolizje = 'Collisions.csv'
    def __str__(self):
        opis = """Objaśnienie danych: \n
        DOTKLIWOSC_KOLIZJI -> skutek kolizji - zmiszczenie mienia, ranii, poważnie ranii lub śmiertelnie ranni \n
        TYP_KOLIZJI -> piesi, rowerzyści, zaparkowany samochód lub samochód w ruchu wraz z kierunkiem zderzenia \n
        KIERUNEK_SZCZEGOLY -> kierunek z którego uderzył pojazd powodujący kolizję \n
        UCZESTNICY -> całkowita liczba osób biorących udział w zdarzeniu \n
        SPRAWCA, POSZKODOWAY -> kto był sprawcą, a kto poszkodowanym wg typu uczestnika ruchu \n
        PRZECHODZIEN, PROWERZYSTA, KIEROWCA -> ilość uczestników zdarzenia wg typu uczestnika ruchu \n
        RANNI, POWAZNIE_RANNI, SMIERTELNIE_RANNI -> ilość poszkodowanych w zdarzeniu wg stopnia obrażeń \n
        NIEUWAGA -> kolizje spowodwane rozkojarzeniem kierującego \n
        POD_WYPLYWEM -> kolizje spowodawane przez osobę pod wplywem środków odurzających \n
        PRZEKORCZENIE_PREDKOSCI -> zdarzenia wnikające ze zbyt brawurowej jazdy \n
        PIERWSZENSTO_PIESZEGO -> potrącenia pieszych, gdy mieli oni pierszewństwo przejścia \n
        POGODA, WARUNKI_DROGOWE, OSWIETLENIE -> warunki pogodowe, drogowe w jakich zdarzyła się kolizja"""
        return opis

def import_data(path=Dataset.kolizje):
    print('Wyciągnięcie i dostosowanie danych chwilę trwa, zrelaksuj się i czekaj na komunikat o zakończeniu')
    warnings.filterwarnings('ignore')
    # ze względu na wielkość danych ładowanie tylko kolumn używanych do analizy
    data  = pd.read_csv(path, index_col='OBJECTID', 
                        usecols=['OBJECTID', 'X', 'Y', 'SEVERITYDESC','COLLISIONTYPE','PERSONCOUNT', 
                        'PEDCOUNT', 'PEDCYLCOUNT', 'VEHCOUNT', 'INJURIES', 'SERIOUSINJURIES', 'FATALITIES', 
                        'INCDTTM', 'SDOT_COLDESC', 'INATTENTIONIND', 'UNDERINFL', 'WEATHER', 
                        'ROADCOND', 'LIGHTCOND', 'PEDROWNOTGRNT', 'SPEEDING'])
    # zmiana nazw kolumn na bardziej intuicyjne
    data.columns = ['DLUGOSC', 'SZEROKOSC', 'DOTKLIWOSC_KOLIZJI','TYP_KOLIZJI','UCZESTNICY', 
                    'PRZECHODZIEN', 'PROWERZYSTA', 'KIEROWCA', 'RANNI', 'POWAZNIE_RANNI', 'SMIERTELNIE_RANNI', 
                    'DATA', 'OPIS_ZDARZENIA', 'NIEUWAGA', 'POD_WYPLYWEM', 'POGODA', 
                    'WARUNKI_DROGOWE', 'OSWIETLENIE', 'PIERWSZENSTO_PIESZEGO', 'PRZEKORCZENIE_PREDKOSCI']
    data = cleaning_data(data)
    data = podzial_daty_na_skladowe(data)
    data = wyciągnięcie_danych_z_opisu(data)
    print('Dane gotowe - możesz robić analizy')
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
    df['TYDZIEN'] = df['DATA'].dt.strftime('%Y-%U')
    df['DATA'] = df['DATA'].dt.date

    df['data'] = df.apply(lambda row: datetime.strptime(f"{int(row.ROK)}-{int(row.MIESIAC)}-{int(row.DZIEN)}", '%Y-%m-%d'), axis=1)

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


def checkbox_outlayer(pytanie):
    wybor = widgets.Checkbox(value=False, description=pytanie, dsiabled=False, indent=False)
    return wybor


def outlayer(wartosc, df):
    if wartosc == 0:
        df = df.drop(df[df.RANNI>8].index)
        print('Katastrofy drogowe wykluczone')
    else:
        df = df
        print('Analiza z katastrofami drogowymi')
    return df


def wybor_lat(pytanie):
    lata = widgets.IntRangeSlider(value=[2004, 2020], min=2004, max=2020, step=1, description=pytanie)
    return lata


def zakres_lat(lata, df):
    rok_min = min(lata)
    rok_max = max(lata)
    df = df.loc[(df['ROK'] > rok_min) & (df['ROK'] <= rok_max)]
    print(f'Analiza lat {rok_min} - {rok_max}')
    return df


def widgety(df):
    global df_box, lata, wybor, wskaznik, cecha, button
    df_box = df
    lata = wybor_lat(pytanie='Zakres lat')
    wybor = checkbox_outlayer(pytanie='Uwzględnić katastrofy drogowe (ranni>8)?') 
    wskaznik = widgets.Dropdown(
           options=['UCZESTNICY','PRZECHODZIEN', 'PROWERZYSTA', 'KIEROWCA',
                    'RANNI', 'POWAZNIE_RANNI', 'SMIERTELNIE_RANNI'],
           value='RANNI',
           description='Miara: ')
    cecha = widgets.Dropdown(
        options=['DOTKLIWOSC_KOLIZJI', 'TYP_KOLIZJI', 'NIEUWAGA', 'POD_WYPLYWEM', 'POGODA', 
                 'WARUNKI_DROGOWE', 'OSWIETLENIE', 'PRZEKROCZENIE_PREDKOSCI', 'ROK', 'MIESIAC', 'DZIEN_TYG',
                 'SPRAWCA', 'POSZKODOWANY', 'KIERUNEK_SZCZEGOLY'],
        value='KIERUNEK_SZCZEGOLY',
        description='Grupa:')
    button = widgets.Button(description='Pokaż',)
    return df_box, lata, wybor, wskaznik, cecha, button


def rysuj_boxplot(df, x, y, hue):
    plt.figure(figsize=(20,10))  # rozszerzenie wykresu na całą stronę
    sns.boxplot(data=df, x=x, y=y, hue=hue, orient="h")  # rysowanie wykresu skrzykowego
    
    
def zarzuc_boxplot(df_box, lata, wybor, wskaznik, cecha, b=None):
    df_analiza = outlayer(wybor.value, df_box)
    df_boxplot = zakres_lat(lata.value, df_analiza)
    miara = wskaznik.value
    grupa = cecha.value
    df_kolizje = df_boxplot.groupby(['DATA',grupa])[miara].agg(WYPADKI='count', RANNI='sum').reset_index()
    df_kolizje.rename(columns={"RANNI": miara}, inplace=True)
    df_long = pd.melt(df_kolizje, 
                  id_vars=cecha.value, var_name='miara',
                  value_vars=['WYPADKI', miara], value_name='suma per dzień')
    
    rysuj_boxplot(df_long, x='suma per dzień', y=grupa, hue='miara')
    
        
def clicked(b):
    zarzuc_boxplot(df_box, lata, wybor, wskaznik, cecha)


def wybierz_zmienne(lata, wybor, wskaznik, cecha, button):
    tab1 = VBox(children=[wybor, lata,])
    tab2 = VBox(children=[wskaznik, cecha,])
    tab = widgets.Tab(children=[tab1, tab2])
    tab.set_title(0, 'zakres danych')
    tab.set_title(1, 'boxplot')
    box = VBox(children=[tab, button])
    return box
    

def prognozy(df):                                                                                                                   
    df_prognozy = df.reset_index()
    df_prognozy['point'] = list(zip(df_prognozy.SZEROKOSC , df_prognozy.DLUGOSC))
    df_prognozy['tydzien'] = df_prognozy['data'].dt.strftime('%Y-%U')
    df_prognozy.drop(df_prognozy[df_prognozy['ROK'] == 2003].index, inplace = True)
    df_prognozy.drop(df_prognozy[df_prognozy['ROK'] == 2020].index, inplace = True)

    return df_prognozy


    