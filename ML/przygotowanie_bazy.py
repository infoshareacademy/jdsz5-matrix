import pandas as pd
import warnings

class Dataset:
    uber = 'rideshare_kaggle.csv'
    def __str__(self):
        opis = """Objaśnienie danych: \n
        cos cos cos jesze nie wiem co \n"""
        return opis

def przygotuj_dane(path=Dataset.uber):
    print('Wyciągnięcie i dostosowanie danych')
    warnings.filterwarnings('ignore')
    # ze względu na wielkość danych ładowanie tylko niezbędnych kolumn
    # usunięte id, timestamp, product_id, long_summary, lat., lon.
    data  = pd.read_csv(path, usecols=['hour', 'datetime',
       'source', 'destination', 'cab_type', 'name', 'price',
       'distance', 'surge_multiplier', 'temperature',
       'apparentTemperature', 'short_summary',
       'precipIntensity', 'precipProbability', 'humidity', 'windSpeed',
       'windGust', 'windGustTime', 'visibility', 'temperatureHigh',
       'temperatureHighTime', 'temperatureLow', 'temperatureLowTime',
       'apparentTemperatureHigh', 'apparentTemperatureHighTime',
       'apparentTemperatureLow', 'apparentTemperatureLowTime', 'icon',
       'dewPoint', 'pressure', 'windBearing', 'cloudCover', 'uvIndex',
       'visibility.1', 'ozone', 'sunriseTime', 'sunsetTime', 'moonPhase',
       'precipIntensityMax', 'uvIndexTime', 'temperatureMin',
       'temperatureMinTime', 'temperatureMax', 'temperatureMaxTime',
       'apparentTemperatureMin', 'apparentTemperatureMinTime',
       'apparentTemperatureMax', 'apparentTemperatureMaxTime'])
    # usunięcie taxi bez ceny
    df = data.dropna()
    # zmiana nazwy zmiennej, która może powodować kłopoty
    df['visibility2'] = df['visibility.1']
    # dodanie nazwy dnia tygodnia
    df['week_day'] = pd.to_datetime(df['datetime']).dt.day_name()
    # zgrupowanie pory dnia z godzin
    dzien_wolny = ['Saturday','Sunday']
    df.loc[df['week_day'].isin(dzien_wolny), 'typ_dnia'] = 'dzien_wolny'
    df.loc[~df['week_day'].isin(dzien_wolny), 'typ_dnia'] = 'dzien_roboczy'
    # zgrupowanie pory dnia z godzin
    godziny_szczytu = [7, 8, 9, 15, 16, 17]
    poza_szczytem = [10, 11, 12, 13, 14, 18, 19]
    noc = [20, 21, 22, 23, 24, 0, 1, 2, 3, 4, 5, 6]
    df.loc[df['hour'].isin(godziny_szczytu), 'pora_dnia'] = 'godziny_szczytu'
    df.loc[df['hour'].isin(poza_szczytem), 'pora_dnia'] = 'godziny_poza_szczytem'
    df.loc[df['hour'].isin(noc), 'pora_dnia'] = 'noc'
    # usunięcie zbędnych kolumn
    df.drop(['datetime', 'visibility.1'], axis=1, inplace=True)
    # zawężenie do ubera
    df_uber = df[df['cab_type'] == 'Uber']
    print('Dane gotowe - możesz iść dalej')
    return df_uber

print(Dataset())
df = przygotuj_dane(Dataset.uber)
df.info()

df.to_csv('uber_clean_data.csv')
