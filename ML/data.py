import pandas as pd
import datetime

# wczytanie danych 'listings.csv'
listings = pd.read_csv('listings.csv')

# Przygotowanie pliku listings. 
# Wstępne usunięcie zbędnych kolumn (opisy tekstowe, brak danych, nieistotne dane)

columns_name = listings.columns

list_columns_to_drop = ['listing_url', 'scrape_id', 'last_scraped', 'name', 'summary', 'space', 'description',
                        'experiences_offered', 'neighborhood_overview', 'notes', 'transit', 'thumbnail_url',
                        'medium_url', 'picture_url', 'xl_picture_url', 'host_id', 'host_url', 'host_name',
                        'host_since', 'host_location', 'host_about', 'host_response_time', 'host_response_rate', 
                        'host_acceptance_rate', 'host_is_superhost', 'host_thumbnail_url', 'host_picture_url', 
                        'host_neighbourhood', 'host_listings_count', 'host_total_listings_count', 
                        'host_verifications', 'host_has_profile_pic', 'host_identity_verified', 'street', 
                        'neighbourhood', 'neighbourhood_cleansed', 'neighbourhood_group_cleansed',
                        'city', 'state', 'market', 'smart_location', 'country_code', 'country',
                        'latitude', 'longitude', 'is_location_exact', 'room_type', 'bed_type', 
                        'amenities','square_feet', 'weekly_price', 'monthly_price', 'security_deposit', 
                        'minimum_nights', 'maximum_nights', 'calendar_updated', 'has_availability', 
                        'availability_30', 'availability_60', 'availability_90', 'availability_365', 
                        'calendar_last_scraped', 'number_of_reviews', 'first_review', 'last_review', 
                        'requires_license', 'review_scores_rating', 'review_scores_accuracy', 
                        'review_scores_cleanliness', 'review_scores_checkin', 'review_scores_communication', 
                        'review_scores_location', 'review_scores_value', 'license', 'jurisdiction_names', 
                        'instant_bookable', 'cancellation_policy', 'require_guest_profile_picture', 
                        'require_guest_phone_verification', 'calculated_host_listings_count', 'reviews_per_month'
                        ]

listings_preliminary_drop = listings.drop(columns=list_columns_to_drop)

# Poprawienie formatu zmiennej 'cleaning_fee'

listings_preliminary_drop['cleaning_fee'] = listings_preliminary_drop['cleaning_fee'].str.replace('$', '')
listings_preliminary_drop['cleaning_fee'] = listings_preliminary_drop['cleaning_fee'].str.replace(',', '')
listings_preliminary_drop['cleaning_fee'] = listings_preliminary_drop['cleaning_fee'].astype(float)

# Zmiana zmiennej 'extra_people' na zmienną kategoryczną

def extra_people_fee(row):
    if row['extra_people'] == '$0.00':
        return 0
    else:
        return 1

listings_preliminary_drop['extra_people'] = listings_preliminary_drop.apply(lambda row: extra_people_fee(row), axis=1)

# Usunięcie wszystkich wierszy z wartością NaN

listings_preliminary_drop = listings_preliminary_drop.dropna()

# Poprawienie formatu zmiennej 'price'

listings_preliminary_drop['price'] = listings_preliminary_drop['price'].str.replace('$', '')
listings_preliminary_drop['price'] = listings_preliminary_drop['price'].astype(float)

# Zastosowanie funkcji get_dummies do zmiennych 'property_type' i 'zipcode'

property_type_dummies = pd.get_dummies(listings_preliminary_drop['property_type'])
zipcode_dummies = pd.get_dummies(listings_preliminary_drop['zipcode'])

listings_prep = listings_preliminary_drop.join(property_type_dummies)
listings_prep = listings_prep.join(zipcode_dummies)

listings_prep = listings_prep.drop(['property_type', 'zipcode'], axis=1)

# Ostatyczny, przygotowany zbiór danych z pliku listings.

listings_after_preparation = listings_prep.rename(columns={'price': 'const_price', 'Bed & Breakfast': 
                                                           'Bed_Breakfast', 'Camper/RV': 'Camper_RV'})


#############################################################################################################


# Wczytanie danych z pliku calendar.
calendar_prep = pd.read_csv('calendar.csv')

# Przygotowanie danych.

# Zmiana formatów zmiennych.
calendar_prep = calendar_prep.rename(columns={'listing_id': 'id'})

calendar_prep['price'] = calendar_prep['price'].str.replace('$', '')
calendar_prep['price'] = calendar_prep['price'].str.replace(',', '')
calendar_prep['price'] = calendar_prep['price'].astype(float)

calendar_prep['date'] = pd.to_datetime(calendar_prep['date'], errors='coerce')

calendar_prep['available'] = calendar_prep['available'].apply(lambda x:1 if x=='t' else 0)

# Zgrupowanie według id i zsumowanie ilości dni, w których lakal był dostępny
calendar_prep['sum_available'] = calendar_prep['available'].groupby(calendar_prep['id']).transform('sum')

# Usunięcie lakali, w których dostępność była powyżej 356 dni i poniżej 9 dni.
calendar_prep.drop(calendar_prep[calendar_prep.sum_available < 9].index, inplace=True)
calendar_prep.drop(calendar_prep[calendar_prep.sum_available > 356].index, inplace=True)

# Uzupełnienie danych zmiennej 'price' o wartości ceny, z dnia poprzedniego lub następnego.
calendar_prep['price'] = calendar_prep.groupby('id')['price'].fillna(method='ffill')
calendar_prep['price'] = calendar_prep.groupby('id')['price'].fillna(method='bfill')
#calendar_group = calendar_prep.groupby(by=['id', 'month']).mean()['price']

# Stworznie kolumny identyfikującej miesiąc z daty
calendar_prep['month'] = calendar_prep['date'].dt.month_name()

# Pogrupowanie według indeksu i miesiąca oraz wyznaczenie średniej dla danego lokalu i miesiąca
calendar_group = calendar_prep.groupby(by=['id', 'month']).mean()['price']


# 
calendar_group = calendar_group.reset_index()
calendar_group['price'] = calendar_group['price'].round()

# Zastosowanie funkcji get_dummies do zmiennej 'month'
month_dummies = pd.get_dummies(calendar_group['month'])
column_month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
month_dummies = month_dummies.reindex(columns=column_month_names)
calendar_after_preparation = calendar_group.join(month_dummies)

# Ostateczny, przygotowany zbiór danych z pliku calendar 
calendar_after_preparation = calendar_after_preparation.drop('month', axis=1)
calendar_after_preparation = calendar_after_preparation.rename(columns={'price': 'Price'})


#############################################################################################################


# Połączenie przygotowanych zbiorów danych z pliku listings i calendar
data = pd.merge(left=calendar_after_preparation, right=listings_after_preparation, how='inner', on='id')

data = data.drop(['id', 'const_price'], axis=1)

# Zapisanie zbioru danych w formacie csv
#data.to_csv('data.csv', index=False)

#############################################################################################################


# Podział zbioru danych na X i y (target)
y = data.Price
X = data.drop('Price', axis=1)

# Podział zbioru danych na zbiór trenigowy i testowy
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
