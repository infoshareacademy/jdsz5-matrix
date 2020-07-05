# na podstawie:
# https://towardsdatascience.com/the-5-feature-selection-algorithms-every-data-scientist-need-to-know-3a6b566efd2
# https://www.kaggle.com/mlwhiz/feature-selection-using-football-data/notebook
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")

##############################################################################
# przygotowanie bazy pod sprawdzenie istotności zmiennych
class Dataset:
    airbnb = 'listings.csv'
    kalendarz = 'calendar.csv'
    def __str__(self):
        opis = """Badanie rynku airbnb, od czego zależy cena wynajmu mieszkania \n"""
        return opis

def przygotuj_dane(path=Dataset.airbnb):
    print('Wyciągnięcie i dostosowanie danych')
    warnings.filterwarnings('ignore')
    # ze względu na wielkość danych ładowanie tylko niezbędnych kolumn
    # usunięte id, timestamp, product_id, long_summary, lat., lon.
    df = pd.read_csv(path)
    # usuwanie zmiennych których nie bierzemy do modelu
    df.drop(['listing_url', 'latitude', 'longitude', 'transit',
             'scrape_id', 'last_scraped', 'calendar_updated','calendar_last_scraped', # jest jedna data 2016-01-04
             'license', 'experiences_offered', # puste kolumny
             'name', 'summary', 'space', 'neighborhood_overview', 'notes', 'description', # dane opisowe długie
             'thumbnail_url', 'medium_url', 'picture_url', 'xl_picture_url', 'host_url', # adresy  url
             'host_id', 'host_name', 'host_location', 'host_about', 'host_neighbourhood',
             'host_thumbnail_url', 'host_picture_url', 'host_verifications',
             'host_response_rate', 'host_acceptance_rate', # dużo pustych wartości
             'host_listings_count', 'host_total_listings_count', 'host_has_profile_pic', 'host_identity_verified', 
             'maximum_nights', # bzdurne wartości
             'require_guest_profile_picture', 'require_guest_phone_verification',
             'street', 'city', 'state', 'market', 'smart_location', 'country_code', 'country',
             'amenities',  # lista udogodnień - długa
             'has_availability', # wszsze jest "t"
             'beds', # jest silnie skorelowane z accomodates
             'availability_30', 'availability_60', 'availability_90',
             'requires_license', # wszędzie jest "f"
             'jurisdiction_names', # tylko WASHINGTON
             'reviews_per_month', # jest iloc per rok, to jest tylko podział na 12 mc - bez znaczenia
             'square_feet', # za mało obserwacji tylko 97 miejscowek mialo to pdane
             'first_review', 'last_review',
             'neighbourhood', 'zipcode', 'neighbourhood_cleansed', # za dużo zmiennych
             'weekly_price', 'monthly_price',
             'is_location_exact',
             'review_scores_accuracy', 'review_scores_cleanliness', 'review_scores_checkin', 
             'review_scores_communication', 'review_scores_location', 'review_scores_value', # miary które są składową głównego ratingu
             'calculated_host_listings_count'], axis=1, inplace=True)
    
    # iloć lat doświadczenia hosta
    df['host_since'] = pd.to_datetime(df['host_since'])
    df['host_experience'] = 2016 - df['host_since'].dt.year
    
    # dodanie cen dla tyogodnia i miesiąca
    #df[df.columns['price', 'weekly_price']] = df[df.columns['price', 'weekly_price']].replace('[\$,]', '', regex=True)
    df['price'] = pd.to_numeric(df['price'].str.replace(',', '').str.replace('$', ''))
    df['security_deposit'] = pd.to_numeric(df['security_deposit'].str.replace(',', '').str.replace('$', '')) 
    df['security_deposit'].fillna(value=0, inplace = True)
    df['cleaning_fee'] = pd.to_numeric(df['cleaning_fee'].str.replace(',', '').str.replace('$', '')) 
    df['cleaning_fee'].fillna(value=0, inplace = True)
    df['extra_people'] = pd.to_numeric(df['extra_people'].str.replace(',', '').str.replace('$', '')) 
    df['extra_people'].fillna(value=0, inplace = True)
    df['extra_people'] = np.where((df['extra_people'] == 0), 0, 1)
    
    # prognozowana wielkość popytu - ilość dni wynajmownych
    df['demand'] = 365 - df['availability_365']
    
    # rekordy t=1, f=0
    df = df.replace({'t': 1, 'f': 0})
    
    # procenty na liczby float
    #df['host_response_rate'] = df['host_response_rate'].str.rstrip('%').astype('float') / 100.0
    #df['host_acceptance_rate'] = df['host_acceptance_rate'].str.rstrip('%').astype('float') / 100.0
  
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
    df2.drop(['host_since', 'availability_365', 'host_response_time', 
             'property_type', 'room_type', 'bed_type', 'cancellation_policy',
             'neighbourhood_group_cleansed'], axis=1, inplace=True)
    
    # poprawienie nazw kolumn po dummifikacji
    df2.columns = df2.columns.str.replace(' ', '').str.replace('_', '').str.replace('&', '').str.replace('\\', '').str.replace('/', '').str.replace('-', '')
    listing_after_prep = df2.dropna()

    listing_after_prep.to_csv('airbnb_clean_data.csv')

    print('Listing gotowe')
    return listing_after_prep

print(Dataset())
df = przygotuj_dane(Dataset.airbnb)

##############################################################################
#szukanie zmiennych do modelu
 # normalizacja
y = df.price
X = df.drop('price', axis=1)
X_norm = pd.DataFrame(StandardScaler().fit_transform(X), columns = X.columns)
X = X_norm



#data = pd.read_csv('airbnb_database.csv')
#data = data.drop(["Unnamed: 0"], axis=1)

#y = data.price
#X = data.drop('price', axis=1)
#X_norm = MinMaxScaler().fit_transform(X)
#X = X_norm

feature_name = list(X.columns)
num_feats  = 10 # ilość zmiennych jakie mają być oznaczoen jako najlesze w danej metodzie

print('\n RFECV')
# wybór zmienych do modelu przy pomocy modelu redukcji modelu
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFECV
rfecv_selector = RFECV(LinearRegression())
rfecv_selector = rfecv_selector.fit(X, y)
print(f'Optymalna liczba zmiennych: {rfecv_selector.n_features_}')

print('\n Pearson correlation')
def cor_selector(X, y, num_feats):
    cor_list = []
    feature_name = X.columns.tolist()
    # calculate the correlation with y for each feature
    for i in X.columns.tolist():
        cor = np.corrcoef(X[i], y)[0, 1]
        cor_list.append(cor)
    # replace NaN with 0
    cor_list = [0 if np.isnan(i) else i for i in cor_list]
    # feature name
    cor_feature = X.iloc[:,np.argsort(np.abs(cor_list))[-num_feats:]].columns.tolist()
    # feature selection? 0 for not select, 1 for select
    cor_support = [True if i in cor_feature else False for i in feature_name]
    return cor_support, cor_feature
cor_support, cor_feature = cor_selector(X, y, num_feats)
print(str(len(cor_feature)), 'selected features')
#print(cor_feature)

#print('\n Chi-Square Features')
#from sklearn.feature_selection import SelectKBest
#from sklearn.feature_selection import chi2
#chi_selector = SelectKBest(chi2, k=num_feats)
#chi_selector.fit(X_norm, y)
#chi_support = chi_selector.get_support()
#chi_feature = X.loc[:,chi_support].columns.tolist()
#print(str(len(chi_feature)), 'selected features')
#print(chi_feature)

print('\n Recursive Feature Elimination')
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
rfe_selector = RFE(estimator=LogisticRegression(), n_features_to_select=num_feats, step=10, verbose=5)
rfe_selector.fit(X, y)
rfe_support = rfe_selector.get_support()
rfe_feature = X.loc[:,rfe_support].columns.tolist()
print(str(len(rfe_feature)), 'selected features')
#print(rfe_feature)

print('\n Lasso: SelectFromModel')
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
embeded_lr_selector = SelectFromModel(LogisticRegression(penalty="l1"), max_features=num_feats)
embeded_lr_selector.fit(X, y)
embeded_lr_support = embeded_lr_selector.get_support()
embeded_lr_feature = X.loc[:,embeded_lr_support].columns.tolist()
print(str(len(embeded_lr_feature)), 'selected features')
#print(embeded_lr_feature)

print('\n Tree-based: SelectFromModel')
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import RandomForestClassifier
embeded_rf_selector = SelectFromModel(RandomForestClassifier(n_estimators=100), max_features=num_feats)
embeded_rf_selector.fit(X, y)
embeded_rf_support = embeded_rf_selector.get_support()
embeded_rf_feature = X.loc[:,embeded_rf_support].columns.tolist()
print(str(len(embeded_rf_feature)), 'selected features')
#print(embeded_rf_feature)

print('\n LightGBM: SelectFromModel')
from sklearn.feature_selection import SelectFromModel
from lightgbm import LGBMClassifier

lgbc=LGBMClassifier(n_estimators=500, learning_rate=0.05, num_leaves=32, colsample_bytree=0.2,
            reg_alpha=3, reg_lambda=1, min_split_gain=0.01, min_child_weight=40)
embeded_lgb_selector = SelectFromModel(lgbc, max_features=num_feats)
embeded_lgb_selector.fit(X, y)
embeded_lgb_support = embeded_lgb_selector.get_support()
embeded_lgb_feature = X.loc[:,embeded_lgb_support].columns.tolist()
print(str(len(embeded_lgb_feature)), 'selected features')
#print(embeded_lgb_feature)

# put all selection together
#feature_selection_df = pd.DataFrame({'Feature':feature_name, 'Pearson':cor_support, 'Chi-2':chi_support, 'RFE':rfe_support, 'Logistics':embeded_lr_support,
 #                                   'Random Forest':embeded_rf_support, 'LightGBM':embeded_lgb_support})
feature_selection_df = pd.DataFrame({'Feature':feature_name, 'Pearson':cor_support, 'RFE':rfe_support, 'Logistics':embeded_lr_support,
                                    'Random Forest':embeded_rf_support, 'LightGBM':embeded_lgb_support})
# count the selected times for each feature
feature_selection_df['Total'] = np.sum(feature_selection_df, axis=1)
# display the top 100
feature_selection_df = feature_selection_df.sort_values(['Total','Feature'] , ascending=False)
feature_selection_df.index = range(1, len(feature_selection_df)+1)
#print(feature_selection_df.head(num_feats))

feature_selection_df.to_csv('feature_selection_df.csv')

# korelacja wybranych zmiennych na mapie ciepła
print('\n Korelacja i heat map na ograniczonym zestawie danych')
variables = ['price', 'accommodates', 'roomtypeEntirehomeapt', 'bedrooms', 
              'securitydeposit', 'roomtypePrivateroom', 
              'numberofreviews', 'hostexperience', 'guestsincluded', 'extrapeople',
               'bathrooms', 'roomtypeSharedroom', 'cleaningfee', 'cancellationpolicystrict']
data = df[df.columns.intersection(variables)]

import seaborn as sns
import matplotlib.pyplot as plt
#get correlations of each features in dataset
corrmat = data.corr()
top_corr_features = corrmat.index
plt.figure(figsize=(20,20))
#plot heat map
sns.heatmap(data[top_corr_features].corr(),annot=True,cmap="RdYlGn")
