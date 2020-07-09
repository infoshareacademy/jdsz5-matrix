import ipywidgets as widgets
from ipywidgets import Layout
from IPython.display import display, clear_output
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
import xgboost as xgb
import functools

style = {'description_width': 'initial'}
#słownik
#miesiace = [(1, 'January'),(2,'February'),(3,'March'),(4,'April'),(5,'May'),(6,'June'),(7,'July'),(8,'August'),(9,'September'),(10,'October'),(11,'November'),(12,'December')]
months = ['January','February','March','April','May','June','July','August','September','October','November','December']
property = ['Apartment','Bed_Breakfast','Boat','Bungalow','Cabin','Camper_RV','Chalet','Condominium','House','Loft','Other','Townhouse','Yurt']
room = ['Entire_Home_apt','Private_room','Shared_room']
zip_code = ['98101','98102','98103','98104','98105','98106','98107','98108','98109','98112','98115','98116','98117','98118','98119','98121','98122','98125','98126','98133','98134','98136','98144','98146','98177','98178','98199']
#clik_miesiac = widgets.IntSlider(description='Miesiąc:', value=1, min=1, max=12)
#clik_miesiac = widgets.Dropdown(description='Miesiąc:', options=miesiace)
clik_month = widgets.SelectionSlider(description='Month:', options=months, value='January', disabled=False, 
                        continuous_update=False, orientation='horizontal', readout=True)
#clik_property = widgets.Dropdown(description='Property type:', options=property, style=style)
clik_property = widgets.Select(description='Property type:', options=property, style=style, rows=len(property))
#clik_room = widgets.RadioButtons(description='Room type:', options=room)
clik_room = widgets.ToggleButtons(description='Room type:', options=room)
clik_guests = widgets.IntSlider(description='Guest included', value=0, min=0, max=10, style=style) # w danych jest max 7
clik_extra_people = widgets.Checkbox(value=False, description='Extra people', disabled=False, style=style)
clik_cleaning = widgets.IntSlider(description='Cleanig fee', value=50, min=1, max=200, style=style)
clik_zip_code = widgets.Select(description='Zip code:', options=zip_code, disabled=False, rows=13, layout=Layout(width='auto'))
clik_bedrooms = widgets.IntSlider(description='Bedrooms:', value=1, min=1, max=5, style=style) # w danych jest max 4
clik_beds = widgets.IntSlider(description='Beds:', value=1, min=1, max=10, style=style) # w danych jest max 7 łóżek
clik_bathrooms = widgets.IntSlider(description='Bathrooms:', value=1, min=0, max=5, style=style)  # w dnych jest max 3,5
clik_accommodates = widgets.IntSlider(description='Accommodates:', value=1, min=1, max=10, style=style) # w danych jest max 7
clik_nights = widgets.IntSlider(description='Minimum nights', value=1, min=1, max=31, style=style) 

clik_model = widgets.ToggleButtons(description='ML MODEL:', options=['xgboost', 'random_forest'])

def xgboost_model():
    df = pd.read_csv('../data/data_minus_outliers_20200708_min.csv')
    y = df.Price.values
    X = df.drop('Price', axis=1)
    X = pd.DataFrame(StandardScaler().fit_transform(X), columns = X.columns)
    testSize = 0.2
    randomState = 0
    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=testSize, random_state=randomState)

    xg_model = xgb.XGBRegressor(objective="reg:squarederror",
                                n_estimators=245,
                                booster='gbtree',
                                max_depth= 10,
                                eta= 0.1,
                                learning_rate= 0.2,
                                min_child_weight= 3,
                                gamma=1,
                                colsample_bytree = 0.9, 
                                colsample_bylevel = 0.9,
                                colsample_bynode = 1,
                                subsample= 1,
                                reg_lambda=1,
                                reg_alpha=100,#alpha = 10
                                max_delta_step=0,
                                tree_method='auto')
    model = xg_model.fit(X_train, Y_train)
    return(model)

def formularz():
    # ostateczna ramka
    box_inside_left = widgets.HBox([clik_zip_code, clik_property])
    left_box = widgets.VBox([clik_model, box_inside_left, clik_room])
    #left_box = widgets.VBox([clik_zip_code, clik_month, clik_room, clik_property])
    right_box = widgets.VBox([clik_month, clik_nights, clik_cleaning, clik_accommodates, clik_beds, clik_bedrooms, clik_bathrooms, clik_guests, clik_extra_people])
    box = widgets.HBox([left_box, right_box])
    #pokaż
    display(box)
    
def click_button_moj(button_moj):
    df_preds = pd.read_csv('../data/testy.csv')
    df_preds[clik_month.value] = 1
    df_preds[clik_property.value] = 1
    df_preds[clik_room.value] = 1
    df_preds[clik_zip_code.value] = 1
    df_preds['accommodates'] = clik_accommodates.value
    df_preds['bathrooms'] = clik_bathrooms.value
    df_preds['bedrooms'] = clik_bedrooms.value
    df_preds['beds'] = clik_beds.value
    df_preds['cleaning_fee'] = clik_cleaning.value
    df_preds['guests_included'] = clik_guests.value
    df_preds['extra_people'] = clik_extra_people.value
    df_preds['minimum_nights'] = clik_nights.value
    print(f'\nZip code: {clik_zip_code.value}, Month: {clik_month.value}, Property type: {clik_property.value}, Room type: {clik_room.value}')
    print(f'Minimum nights: {clik_nights.value}, Accommodates: {clik_accommodates.value}, Bathrooms: {clik_bathrooms.value}, Bedrooms: {clik_bedrooms.value}, Beds: {clik_beds.value}')
    print(f'Cleaning_fees: {clik_cleaning.value}, Guests_included: {clik_guests.value}, Extra_people: {clik_extra_people.value}')
    xgboost_calosc(df_preds)

def oblicz_cene(model):
    df_preds = pd.read_csv('../data/testy.csv')
    df_preds[clik_month.value] = 1
    df_preds[clik_property.value] = 1
    df_preds[clik_room.value] = 1
    df_preds[clik_zip_code.value] = 1
    df_preds['accommodates'] = clik_accommodates.value
    df_preds['bathrooms'] = clik_bathrooms.value
    df_preds['bedrooms'] = clik_bedrooms.value
    df_preds['beds'] = clik_beds.value
    df_preds['cleaning_fee'] = clik_cleaning.value
    df_preds['guests_included'] = clik_guests.value
    df_preds['extra_people'] = clik_extra_people.value
    df_preds['minimum_nights'] = clik_nights.value
    print(f'\nZip code: {clik_zip_code.value}, Month: {clik_month.value}, Property type: {clik_property.value}, Room type: {clik_room.value}')
    print(f'Minimum nights: {clik_nights.value}, Accommodates: {clik_accommodates.value}, Bathrooms: {clik_bathrooms.value}, Bedrooms: {clik_bedrooms.value}, Beds: {clik_beds.value}')
    print(f'Cleaning_fees: {clik_cleaning.value}, Guests_included: {clik_guests.value}, Extra_people: {clik_extra_people.value}')
    xgboost_check(df_preds, model)

def xgboost_check(df_preds, model):
    preds = model.predict(df_preds)
    print(f'Przewidywana cena: {preds}')


def xgboost_calosc(df_preds):
    df = pd.read_csv('../data/data_minus_outliers_20200708_min.csv')
    y = df.Price.values
    X = df.drop('Price', axis=1)
    X = pd.DataFrame(StandardScaler().fit_transform(X), columns = X.columns)
    testSize = 0.2
    randomState = 0
    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=testSize, random_state=randomState)

    xg_model = xgb.XGBRegressor(objective="reg:squarederror",
                                n_estimators=325,
                                booster='gbtree',
                                max_depth= 10,
                                eta= 0.2,
                                learning_rate= 0.2,
                                min_child_weight= 3,
                                gamma=0.9,
                                colsample_bytree = 0.9, 
                                colsample_bylevel = 1,
                                colsample_bynode = 1,
                                subsample= 1,
                                reg_lambda=1,
                                reg_alpha=100,#alpha = 10
                                max_delta_step=0,
                                tree_method='auto')
    xg = xg_model.fit(X_train, Y_train)
    preds = xg.predict(df_preds)
    print(f'Przewidywana cena: {preds}')

def click_button_model(button_model):
    print(f'Wybrałeś model: {clik_model.value}')








