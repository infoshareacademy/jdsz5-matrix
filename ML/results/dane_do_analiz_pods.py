import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
import folium
from folium import plugins
import plotly.express as px
import seaborn as sns
#import geopandas as gpd
from sklearn import cluster
from sklearn.preprocessing import scale
from sklearn.cluster import KMeans

class Dataset:
    airbnb = 'listings.csv'
    najem = 'calendar.csv'
    def __str__(self):
        opis = """Objaśnienie danych: \n
        Oto zestaw danych, które zostały wykorzystane w projekcie: \n"""
        return opis

def przygotuj_dane_pods(path=Dataset.airbnb):
    print('Wyciągnięcie i dostosowanie danych')
    warnings.filterwarnings('ignore')
    # ze względu na wielkość danych ładowanie tylko niezbędnych kolumn
    # usunięte id, timestamp, product_id, long_summary, lat., lon.
    df_b  = pd.read_csv(path)
    # usuwanie zmiennych których nie bierzemy do modelu
    df_b.drop(['listing_url', 
         'last_scraped', # jest jedna data 2016-01-04
         'scrape_id', 
         'license', # pusta kolumna
         'name', # nazwa ogłoszenia
         'summary', # podsumowanie
         'space', # opis miejsca
         'experiences_offered', # cała kolumna pusta
         'neighborhood_overview', #opis okolicy
         'notes',
         'transit', 
         'thumbnail_url',
         'medium_url',
         'picture_url',
         'xl_picture_url',
         'host_url', 'host_id',
         'host_name', 'host_location',
         'host_about', 'host_neighbourhood',
         'host_thumbnail_url',
         'host_picture_url',
         'host_verifications',
         'street',
         'city',
         'state',
         'market',
         'smart_location',
         'country_code', 'country',
         'amenities',  # lista udogodnień - długa
         'calendar_updated','calendar_last_scraped', # tylko jedna data
         'has_availability', # wszsze jest "t"
         'availability_30', 'availability_60', 'availability_90',
         'requires_license', # wszędzie jest "f"
         'jurisdiction_names', # tylko WASHINGTON
         'reviews_per_month', # jest iloc per rok, to jest tylko podział na 12 mc - bez znaczenia
         'square_feet', # za mało obserwacji tylko 97 miejscowek mialo to pdane
         'first_review', 'last_review',
         'neighbourhood', 'zipcode', # za dużo zmiennych
         'is_location_exact',
         'description'], axis=1, inplace=True)
    
    # iloć lat doświadczenia hosta
    df_b['host_since'] = pd.to_datetime(df_b['host_since'])
    df_b['host_experience'] = 2016 - df_b['host_since'].dt.year
    
    # dodanie cen dla tyogodnia i miesiąca
    df_b['price'] = pd.to_numeric(df_b['price'].str.replace(',', '').str.replace('$', ''))
    df_b['weekly_price'] = pd.to_numeric(df_b['weekly_price'].str.replace(',', '').str.replace('$', ''))    
    df_b['weekly_price'].fillna(value=(df_b['price']*7), inplace = True)
    df_b['monthly_price'] = pd.to_numeric(df_b['monthly_price'].str.replace(',', '').str.replace('$', ''))     
    df_b['monthly_price'].fillna(value=(df_b['price']*30), inplace = True)
    df_b['security_deposit'] = pd.to_numeric(df_b['security_deposit'].str.replace(',', '').str.replace('$', '')) 
    df_b['security_deposit'].fillna(value=0, inplace = True)
    df_b['cleaning_fee'] = pd.to_numeric(df_b['cleaning_fee'].str.replace(',', '').str.replace('$', '')) 
    df_b['cleaning_fee'].fillna(value=0, inplace = True)
    df_b['extra_people'] = pd.to_numeric(df_b['extra_people'].str.replace(',', '').str.replace('$', '')) 
    df_b['extra_people'].fillna(value=0, inplace = True)    
    
    # prognozowana wielkość popytu - ilość dni wynajmownych
    df_b['demand'] = 365 - df_b['availability_365']
    
    # rekordy t=1, f=0
    df_b = df_b.replace({'t': 1, 'f': 0})
    
    # procenty na liczby float
    df_b['host_response_rate'] = df_b['host_response_rate'].str.rstrip('%').astype('float') / 100.0
    df_b['host_acceptance_rate'] = df_b['host_acceptance_rate'].str.rstrip('%').astype('float') / 100.0
    
    # uuń wiersze, jeżel występuje w nim pusty rekord
    df_b.dropna(inplace=True)
    
    # dummifikacja kategorii
    df2 = pd.concat([df_b,
                pd.get_dummies(df_b['host_response_time'], prefix='host_response_time'),
                pd.get_dummies(df_b['property_type'], prefix='property_type'),
                pd.get_dummies(df_b['neighbourhood_group_cleansed'], prefix='neighbourhood_group_cleansed'),
                pd.get_dummies(df_b['room_type'], prefix = 'room_type'), 
                pd.get_dummies(df_b['bed_type'], prefix = 'bed_type'), 
                pd.get_dummies(df_b['cancellation_policy'], prefix = 'cancellation_policy')], 
                axis=1)
    
    #############################################################################################################
    
    # Wczytanie danych z pliku calendar.
    calendar_prep = pd.read_csv('calendar.csv')
    
    # Zmiana formatów zmiennych.
    calendar_prep = calendar_prep.rename(columns={'listing_id': 'id'})

    calendar_prep['price'] = calendar_prep['price'].str.replace('$', '')
    calendar_prep['price'] = calendar_prep['price'].str.replace(',', '')
    calendar_prep['price'] = calendar_prep['price'].astype(float)

    calendar_prep['date'] = pd.to_datetime(calendar_prep['date'], errors='coerce')

    calendar_prep['available'] = calendar_prep['available'].apply(lambda x:1 if x=='t' else 0)

    # Zgrupowanie według id i zsumowanie ilości dni, w których lakal był dostępny
    calendar_prep['sum_available'] = calendar_prep['available'].groupby(calendar_prep['id']).transform('sum')

    # Usunięcie lokali, w których dostępność była powyżej 356 dni i poniżej 9 dni.
    calendar_prep.drop(calendar_prep[calendar_prep.sum_available < 9].index, inplace=True)
    calendar_prep.drop(calendar_prep[calendar_prep.sum_available > 356].index, inplace=True)

    # Uzupełnienie danych zmiennej 'price' o wartości ceny, z dnia poprzedniego lub następnego.
    calendar_prep['price'] = calendar_prep.groupby('id')['price'].fillna(method='ffill')
    calendar_prep['price'] = calendar_prep.groupby('id')['price'].fillna(method='bfill')

    # Stworznie kolumny identyfikującej miesiąc z daty
    calendar_prep['month'] = calendar_prep['date'].dt.month_name()
    calendar_prep['month_no'] = calendar_prep['date'].dt.month
    calendar_prep['day'] = calendar_prep['date'].dt.day_name()
    calendar_prep['day_no'] = calendar_prep['date'].dt.weekday +1

    # Pogrupowanie według indeksu i miesiąca oraz wyznaczenie średniej dla danego lokalu i miesiąca
    calendar_group = calendar_prep.groupby(by=['id', 'month', 'month_no', 'day_no']).mean()['price']

    # 
    calendar_group = calendar_group.reset_index()
    calendar_group['price'] = calendar_group['price'].round()

    # Zastosowanie funkcji get_dummies do zmiennej 'month'
    month_dummies = pd.get_dummies(calendar_group['month'])
    column_month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_dummies = month_dummies.reindex(columns=column_month_names)
    calendar_after_preparation = calendar_group.join(month_dummies)

    # Ostateczny, przygotowany zbiór danych z pliku calendar 
    calendar_after_preparation = calendar_after_preparation.rename(columns={'price': 'Price'})

    #############################################################################################################

    # Połączenie przygotowanych zbiorów danych z pliku listings i calendar
    df2 = pd.merge(left=calendar_after_preparation, right=df2, how='inner', on='id')

    # usuń zbędne kolumny, które potrzebne były tylko do przekształceń
    df2.drop(['id', 'host_since', 'availability_365', 'host_response_time', 
             'room_type', 'bed_type', 'cancellation_policy'], axis=1, inplace=True)
    
    # poprawienie nazw kolumn po dummifikacji
    df2.columns = df2.columns.str.replace(' ', '').str.replace('_', '').str.replace('&', '').str.replace('\\', '').str.replace('/', '').str.replace('-', '')
    
    df2.to_csv('airbnb_data_basic_analysis.csv')
    
    print('Dane gotowe - możesz iść dalej')
    return df2

print(Dataset())
df_b = przygotuj_dane_pods(Dataset.airbnb)
df_b.info()
for col in df_b.columns: 
    print(col)
#print(set(df['neighbourhood_group_cleansed'].unique()))


df_b = pd.read_csv('airbnb_data_basic_analysis.csv')





