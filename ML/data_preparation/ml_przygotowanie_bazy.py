import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt

class Dataset:
    airbnb = 'listings.csv'
    najem = 'calendar.csv'
    def __str__(self):
        opis = """Objaśnienie danych: \n
        cos cos cos jesze nie wiem co \n"""
        return opis

def przygotuj_dane(path=Dataset.airbnb):
    print('Wyciągnięcie i dostosowanie danych')
    warnings.filterwarnings('ignore')
    # ze względu na wielkość danych ładowanie tylko niezbędnych kolumn
    # usunięte id, timestamp, product_id, long_summary, lat., lon.
    df  = pd.read_csv(path)
    # usuwanie zmiennych których nie bierzemy do modelu
    df.drop(['listing_url', 
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
         'neighbourhood', 'zipcode', 'neighbourhood_cleansed', # za dużo zmiennych
         'is_location_exact',
         'description'], axis=1, inplace=True)
    
    # iloć lat doświadczenia hosta
    df['host_since'] = pd.to_datetime(df['host_since'])
    df['host_experience'] = 2016 - df['host_since'].dt.year
    
    # dodanie cen dla tyogodnia i miesiąca
    #df[df.columns['price', 'weekly_price']] = df[df.columns['price', 'weekly_price']].replace('[\$,]', '', regex=True)
    df['price'] = pd.to_numeric(df['price'].str.replace(',', '').str.replace('$', ''))
    df['weekly_price'] = pd.to_numeric(df['weekly_price'].str.replace(',', '').str.replace('$', ''))    
    df['weekly_price'].fillna(value=(df['price']*7), inplace = True)
    df['monthly_price'] = pd.to_numeric(df['monthly_price'].str.replace(',', '').str.replace('$', ''))     
    df['monthly_price'].fillna(value=(df['price']*30), inplace = True)
    df['security_deposit'] = pd.to_numeric(df['security_deposit'].str.replace(',', '').str.replace('$', '')) 
    df['security_deposit'].fillna(value=0, inplace = True)
    df['cleaning_fee'] = pd.to_numeric(df['cleaning_fee'].str.replace(',', '').str.replace('$', '')) 
    df['cleaning_fee'].fillna(value=0, inplace = True)
    df['extra_people'] = pd.to_numeric(df['extra_people'].str.replace(',', '').str.replace('$', '')) 
    df['extra_people'].fillna(value=0, inplace = True)    
    
    # prognozowana wielkość popytu - ilość dni wynajmownych
    df['demand'] = 365 - df['availability_365']
    
    # rekordy t=1, f=0
    df = df.replace({'t': 1, 'f': 0})
    
    # procenty na liczby float
    df['host_response_rate'] = df['host_response_rate'].str.rstrip('%').astype('float') / 100.0
    df['host_acceptance_rate'] = df['host_acceptance_rate'].str.rstrip('%').astype('float') / 100.0
    
    # uuń wiersze, jeżel występuje w nim pusty rekord
    df.dropna(inplace=True)
    
    # dummifikacja kategorii
    df2 = pd.concat([df,
                pd.get_dummies(df['host_response_time'], prefix='host_response_time'),
                pd.get_dummies(df['property_type'], prefix='property_type'),
                pd.get_dummies(df['neighbourhood_group_cleansed'], prefix='neighbourhood_group_cleansed'),
                pd.get_dummies(df['room_type'], prefix = 'room_type'), 
                pd.get_dummies(df['bed_type'], prefix = 'bed_type'), 
                pd.get_dummies(df['cancellation_policy'], prefix = 'cancellation_policy')], 
                axis=1)
    
    
    # usuń zbędne kolumny, które potrzebne były tylko do przekształceń
    df2.drop(['id', 'host_since', 'availability_365', 'host_response_time', 
             'property_type', 'room_type', 'bed_type', 'cancellation_policy',
             'neighbourhood_group_cleansed'], axis=1, inplace=True)
    
    # poprawienie nazw kolumn po dummifikacji
    df2.columns = df2.columns.str.replace(' ', '').str.replace('_', '').str.replace('&', '').str.replace('\\', '').str.replace('/', '').str.replace('-', '')
    
    df2.to_csv('airbnb_clean_data.csv')

    
    print('Dane gotowe - możesz iść dalej')
    return df2

print(Dataset())
df = przygotuj_dane(Dataset.airbnb)
df.info()
#print(set(df['neighbourhood_group_cleansed'].unique()))

