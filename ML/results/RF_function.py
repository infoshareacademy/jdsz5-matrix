import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from datetime import datetime
from csv import DictWriter
import os.path
import matplotlib.pyplot as plt

def RandomForest_model(max_depth,n_estimators):

    df = pd.read_csv('../data/data_ML.csv')
      
    # Target
    y = df['Price'].values
    
    # Data
    X = df.drop('Price', axis=1).values
    
    # Data split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
      
    model = RandomForestRegressor(
        max_depth = max_depth,
        n_estimators = n_estimators,
        random_state = False,
        verbose = False
        )
    
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    r2 = r2_score(y_test, y_pred)
    #print('R2: ', round(r2,3))
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    #print('RMSE: ', round(rmse,3))
    mae = mean_absolute_error(y_test, y_pred)
    #print('MAE: ', round(mae,3))
    
    print('R2: {}, RMSE: {}, MAE: {}'.format(round(r2,2),round(rmse,2),round(mae,2)))