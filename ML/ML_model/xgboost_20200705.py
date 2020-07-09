import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_validate, train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
import xgboost
from xgboost import XGBRegressor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import math
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv('../data/data_minus_outliers_20200708_min.csv')
y = df.Price.values
# bez nomalizacji
#X = df.drop('Price', axis=1).values
# normalizacja
X = df.drop('Price', axis=1)
X = pd.DataFrame(StandardScaler().fit_transform(X), columns = X.columns)
X = X.values

testSize = 0.2
randomState = 0

# dla Real regresji
regrModels = {
    #"linear": LinearRegression(),
    #"logit": LogisticRegression(),
    #"decision_tree": DecisionTreeRegressor(),
    #"random_forest": RandomForestRegressor(),
    "xgboost": XGBRegressor(objective="reg:squarederror"),
    #"bayes": GaussianNB(),
    #"svm": SVR(),
    #"knn": KNeighborsRegressor()
}

regrSplit = (X_train, X_test, Y_train, Y_test) = train_test_split(X, y, test_size=testSize, random_state=randomState)


# poszukiwania najlepszego modelu i zabawa w parametry

tuned_parameters = {
    #"linear": {???},
    #"logit": {'C': [0.1, 1.0, 5.0]},
    #"decision_tree": {'max_depth': [3, 4, 5, 6, 7, 8, 9 ,10]},
    #"random_forest": {'n_estimators': [10, 30, 60, 90, 120]},
    "xgboost": {'n_estimators': [243], #range(250, 325, 25), #[325], range(50, 400, 50)
                'booster': ['gbtree'], #'['gbtree', 'gblinear'],
                #default=6, range: [0,∞]
                'max_depth': [10], # [3, 4, 5, 6, 7, 8, 9 ,10],
                #default=0.3, range: [0,1]
                'eta': [0.1], # [0.1, 0.2, 0.3]
                'learning_rate': [0.2], #'[0.05, 0.1, 0.2, 0.3]
                #default=1, range: [0,∞]
                'min_child_weight': [3], #[1, 2, 3]
                #default=0, range: [0,∞]
                'gamma': [1],#[0.9], # [0, 0.5, 1]
                #default=1, range of (0, 1]
                'colsample_bytree': [0.9], #'colsample_bytree': [1, 0.7, 0.3], potem [0.9, 1]
                'colsample_bylevel': [0.9], #: [1, 0.7, 0.3],[1, 0.9, 0.8]
                'colsample_bynode': [1], #: [1, 0.7, 0.3],[1, 0.9, 0.8]
                #default=1, range: (0,1]
                'subsample': [1], # [1, 0.6, 0.4] teaz to jest do sprawdzenia [0.9, 1]
                #default=1
                'reg_lambda': [1], #[0.1, 1, 10, 100]
                #default=0
                'reg_alpha':[100], #[1e-5, 1e-2, 0.1, 1, 100]
                #default=0, range: [0,∞]
                'max_delta_step': [0], # [0, 5, 10]
                #tree_method string [default= auto]
                'tree_method': ['auto']}, # ['auto', 'exact', 'approx', 'hist', 'gpu_hist'] 
    #"bayes": {'priors': [(0.3, 0.3, 0.4), (0.5, 0.25, 0.25)]},
    #"svm": {"C": [0.1, 0.01, 0.03]},
    #"knn": {"n_neighbors": [3, 5, 7]}
}

best_models = {}
results_csv = pd.DataFrame()

for key in regrModels:
    print(f"Training {key}")
    clf = GridSearchCV(regrModels[key], tuned_parameters[key])
    result = clf.fit(X_train, Y_train)
    best_models[key] = result.best_estimator_
    testScore = clf.score(X_test, Y_test)
    preds = clf.predict(X_test)
    rmse = np.sqrt(mean_squared_error(Y_test, preds))
    mae = mean_absolute_error(Y_test, preds)
    time_string = datetime.now().strftime('%Y%m%d_%H%M%S')
    tmp = pd.DataFrame({'Datetime': time_string, 'Algorithm': key, 'Best_score': clf.best_score_, \
          'Best_params': [clf.best_params_], 'R2': testScore, 'RMSE': rmse, 'MAE': mae})
    results_csv = results_csv.append(tmp)
    # zapis do pliku dla jednego modelu
    results_csv.to_csv("../results/xgboost_results.csv", index=False, sep=';', header=False, mode='a')
    # zapis do pliku dla próby z wszystkimi modelami
    #results_csv.to_csv("tunning_results.csv", index=False, sep=';', header=False, mode='a')
    print(f'Datetime: {time_string}, Algorithm: {key}, Best_score: {clf.best_score_}, \
          Best_params: {clf.best_params_}, R2: {testScore}, RMSE: {rmse}, MAE: {mae}')

##############################################################################
#kawałek kodu dzięki któremu będzie łatwo porównywać wyniki najlepszych tuningów
#results = []

#for key, model in best_models.items():
    #score = model.score(X_test, Y_test)
    #print(key, score)
    #print(model)
    #results.append(score)
    #print(f'Algorithm: {key}, R2: {round(score,2)}')
    
#plt.figure(figsize=(5, 5))
#plt.bar(x=list(best_models.keys()), height=results)
#plt.title("Wyniki testów")




