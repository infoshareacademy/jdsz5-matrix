import pandas as pd
import datetime
import matplotlib.pyplot as plt
import missingno as msno
import math
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import numpy as np

# Przygotowanie bazy danych do Machine Learning.

# Wczytanie bazy danych listings.csv.
listings = pd.read_csv('../data/listings.csv')

# Wstępne usunięcie zbędnych kolumn (opisy tekstowe, brak danych, nieistotne dane)
list_columns_to_drop = ['listing_url', 'scrape_id', 'last_scraped', 'name', 'summary', 'space', 'description',
                        'experiences_offered', 'neighborhood_overview', 'notes', 'transit', 'thumbnail_url',
                        'medium_url', 'picture_url', 'xl_picture_url', 'host_id', 'host_url', 'host_name',
                        'host_location', 'host_about', 'host_response_time', 'host_response_rate', 
                        'host_acceptance_rate', 'host_thumbnail_url', 'host_picture_url', 'availability_365',
                        'host_neighbourhood', 'host_listings_count', 'host_total_listings_count', 
                        'host_verifications', 'host_has_profile_pic', 'host_identity_verified', 'street', 
                        'neighbourhood', 'neighbourhood_cleansed', 'city', 'state', 'market', 'smart_location', 
                        'country_code', 'country', 'latitude', 'longitude', 'is_location_exact', 'amenities',
                        'square_feet', 'weekly_price', 'monthly_price', 'calendar_updated', 'has_availability', 
                        'availability_30', 'availability_60', 'availability_90', 'calendar_last_scraped',
                        'first_review', 'last_review', 'requires_license',  'review_scores_accuracy', 
                        'review_scores_cleanliness', 'review_scores_checkin', 'review_scores_communication', 
                        'review_scores_location', 'review_scores_value', 'license', 'jurisdiction_names', 
                        'instant_bookable',  'require_guest_profile_picture', 'require_guest_phone_verification', 
                        'calculated_host_listings_count', 'reviews_per_month', 'neighbourhood_group_cleansed'
                        ]

listings_preliminary_drop = listings.drop(columns=list_columns_to_drop)

# Poprawienie błędnego kodu pocztowego
unique_zipcode = listings_preliminary_drop['zipcode'].unique()
listings_preliminary_drop.loc[859,'zipcode'] = '98122'

# Dodanie zmiennej host_experience na podstawie zmiennej host_since
listings_preliminary_drop['host_since'] = pd.to_datetime(listings_preliminary_drop['host_since'])
listings_preliminary_drop['host_experience'] = 2016 - listings_preliminary_drop['host_since'].dt.year
listings_preliminary_drop = listings_preliminary_drop.drop('host_since', axis=1)

# Poprawienie formatu zmiennych
listings_preliminary_drop['price'] = listings_preliminary_drop['price'].str.replace('$', '')
listings_preliminary_drop['price'] = listings_preliminary_drop['price'].str.replace(',', '')
listings_preliminary_drop['price'] = listings_preliminary_drop['price'].astype(float)

listings_preliminary_drop['cleaning_fee'] = listings_preliminary_drop['cleaning_fee'].str.replace('$', '')
listings_preliminary_drop['cleaning_fee'] = listings_preliminary_drop['cleaning_fee'].str.replace(',', '')
listings_preliminary_drop['cleaning_fee'] = listings_preliminary_drop['cleaning_fee'].astype(float)

listings_preliminary_drop['security_deposit'] = listings_preliminary_drop['security_deposit'].str.replace('$', '')
listings_preliminary_drop['security_deposit'] = listings_preliminary_drop['security_deposit'].str.replace(',', '')
listings_preliminary_drop['security_deposit'] = listings_preliminary_drop['security_deposit'].astype(float)

listings_preliminary_drop['extra_people'] = listings_preliminary_drop['extra_people'].apply(lambda x:0 if x=='$0.00' else 1)
listings_preliminary_drop['host_is_superhost'] = listings_preliminary_drop['host_is_superhost'].apply(lambda x:1 if x=='t' else 0)

# Uzupełnienie brakujących wartości
listings_preliminary_drop['cleaning_fee'] = listings_preliminary_drop['cleaning_fee'].fillna(0)
listings_preliminary_drop['security_deposit'] = listings_preliminary_drop['security_deposit'].fillna(0)

# Usunięcie kolumny review_scores_rating ze względu na 26% brakujących wartości
listings_second_drop = listings_preliminary_drop.drop('review_scores_rating', axis=1)

# Usunięcie wierszy z wartością NaN
listings_plot_drop = listings_second_drop.dropna()


# Histogramy zmiennych
def drawAllHist(data, histNumInRow,res):
    
    cols_name = data.columns
    
    cols = data.values.shape[1]
    howManyHistRows = math.ceil(cols / histNumInRow)
    fig, axs = plt.subplots(howManyHistRows, histNumInRow, figsize=(20, 20))
    for r in range(histNumInRow):
        for c in range(howManyHistRows):
            idx = int(c * histNumInRow+r)
            if idx < cols:
                axs[c,r].set_title(cols_name[idx])
                axs[c,r].hist(data.values[:, idx],res)
            else:
                break
    plt.tight_layout()
    plt.show()


subplots_histograms = listings_plot_drop.drop(['id', 'zipcode'], axis=1)
subplots_histograms['property_type'] = LabelEncoder().fit_transform(subplots_histograms['property_type'])


# Boxploty zmiennych
def drawAllBoxplot(data, boxNumInRow):

    cols_name = data.columns
    
    cols = data.values.shape[1]
    howManyBoxRows = math.ceil(cols / boxNumInRow)
    fig, axs = plt.subplots(howManyBoxRows, boxNumInRow, figsize=(20, 20))
    for r in range(boxNumInRow):
        for c in range(howManyBoxRows):
            idx = int(c * boxNumInRow + r)
            if idx < cols:
                axs[c,r].set_title(cols_name[idx])
                axs[c,r].boxplot(data.values[:, idx])
            else:
                break
    plt.tight_layout()
    plt.show()


subplots_Boxplots = listings_plot_drop.drop(['id', 'host_is_superhost','zipcode', 'property_type',
                                                    'room_type', 'bed_type', 'extra_people',
                                                    'cancellation_policy'], axis=1)


# Correlation dataframe
heatmap = listings_second_drop.drop(['bed_type', 'cancellation_policy'], axis=1)
heatmap = heatmap.dropna()
listings_second_drop = listings_second_drop.drop(['host_is_superhost', 'bed_type', 'security_deposit', 'maximum_nights', 'number_of_reviews', 'cancellation_policy', 'host_experience'], axis=1)


# Usuwanie outlierów
def rm_out(df,columns=None):
    
    if columns:
        columns = columns
    else:
        columns = df.columns
    
    df_out = df.copy()
    for c in columns:
        q1 = df[c].quantile(0.25)
        q3 = df[c].quantile(0.75)
        IRQ = q3 - q1
        df_out = df_out.loc[(df[c] <= q3 + 1.5 * IRQ) & (df[c] >= q1 - 1.5 * IRQ)]
    df_out.index = range(len(df_out))
    return df_out


listings_second_drop = rm_out(listings_second_drop, columns=['cleaning_fee', 'accommodates'])


listings_second_drop = listings_second_drop.dropna()
listings_second_drop.drop(listings_second_drop['price'].idxmax(), inplace=True)

cols = ['accommodates','bathrooms','bedrooms','beds', 'cleaning_fee', 'extra_people',
        'minimum_nights', 'maximum_nights', 'guests_included', 'number_of_reviews', 'host_experience',
        'price']

#Find out correlation between columns and plot

# Heatmap korelacji zmiennych
def corrHeatmap(df,cols):    
    corrs = np.corrcoef(df[cols].values.T)
    sns.set(font_scale=1)
    sns.set(rc={'figure.figsize':(12,12)})
    hm=sns.heatmap(corrs, cbar = True, annot=True, square = True, fmt = '.2f',
                  yticklabels = cols, xticklabels = cols).set_title('Correlations heatmap')
    return hm


# Zastosowanie funkcji get_dummies do zmiennych 'property_type' i 'zipcode'
property_type_dummies = pd.get_dummies(listings_second_drop['property_type'])
zipcode_dummies = pd.get_dummies(listings_second_drop['zipcode'])
room_type_dummies = pd.get_dummies(listings_second_drop['room_type'])

listings_prep = listings_second_drop.join(property_type_dummies)
listings_prep = listings_prep.join(zipcode_dummies)
listings_prep = listings_prep.join(room_type_dummies)

listings_prep = listings_prep.drop(['property_type', 'zipcode', 'room_type'], axis=1)

# Poprawienie nazw kolumn
listings_after_preparation = listings_prep.rename(columns={'price': 'const_price', 'Bed & Breakfast': 
                                                           'Bed_Breakfast', 'Camper/RV': 'Camper_RV', 'Entire home/apt':
                                                           'Entire_Home_apt', 'Private room': 'Private_room', 'Shared room': 'Shared_room'})
  

###########################################################################################################


# Wczytanie danych z pliku calendar.
calendar_prep = pd.read_csv('../data/calendar.csv')

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

data.drop(data[data['id'].isin([5040885,6362362,7439802,8668410,8811781,757840])].index, inplace=True)

data = data.drop(['id', 'const_price'], axis=1)

#Zapisanie zbioru danych w formacie csv
#data.to_csv('data_ML.csv', index=False)

