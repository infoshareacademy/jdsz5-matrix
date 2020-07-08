import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_validate, train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error
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

regrModels = {
    "linear": LinearRegression(),
    #"logit": LogisticRegression(),
    "decision_tree": DecisionTreeRegressor(),
    "random_forest": RandomForestRegressor(),
    "xgboost": XGBRegressor(objective="reg:squarederror"),
    "bayes": GaussianNB(),
    "svm": SVR(),
    "knn": KNeighborsRegressor()
}

regrSplit = (X_train, X_test, Y_train, Y_test) = train_test_split(X, y, test_size=testSize, random_state=randomState)

# funkcja trenująca model
def trainCV(model, data, target, cv=5):
    """
    funkcja przeprowadzająca krosswalidację oraz zwracająca średnie wartości czasów i score'a
    :param model: model estymatora z pakietu sklearn
    :param data: cechy do przeprowadzenia uczenia
    :param target: wartości wyjściowe
    :param cv: ilość podziałów na krosswalidację, domyślnie 5
    """
    # przeprowadzamy kross walidację i zbieramy wyniki
    results = cross_validate(model, data, target, cv=cv)
    # zwracamy średnie ze wszystkich przebiegów
    outputDict = {
        'meanFitTime': results['fit_time'].mean(),
        'meanScoreTime': results['score_time'].mean(),
        'meanScore':  results['test_score'].mean()
    }
    return outputDict

def printResultsCharts(results, figsize=(15, 20)):
    """
    Wyświetlanie wykresów wyników treningu
    :param results: wyniki treningu w postaci słownika list, np. {
        "modelName": [], <- ta lista musi być zawsze, reszta jest opcjonalna
        "meanScore": [], 
        "meanFitTime": [],
        "meanScoreTime": []}
    """
    # pobieramy listę nazw zawartości
    keys = list(results.keys())
    # tworzymy kontener na wykresy
    axis_number = len(keys)-1
    fig, axs = plt.subplots(axis_number, 1, figsize=figsize)
    if axis_number > 1:
        for i in range(axis_number):
            axs[i].bar(results[keys[0]],results[keys[i+1]])
            axs[i].set_ylabel(keys[i+1])
            axs[i].set_title(keys[i+1])
            axs[i].set_xlabel(keys[0])
    else:
        axs.bar(results[keys[0]],results[keys[1]])
        axs.set_ylabel(keys[1])
        axs.set_title(keys[1])
        axs.set_xlabel(keys[0])
            
def TrainAndPrintResults(modelList, dataset, figsize=(15, 20)):
    """
    funkcja przeprowadzająca trening na liście modeli.
    :param modelList: Lista modeli kompatybilnych z pakietem sklearn
    :param dataset: krotka datasetu po podziale na train i test w postaci (x_train, x_test, y_train, y_test)
    """
    # bierzemy z datasetu dane treningowe
    x_train, x_test, y_train, y_test = dataset
    # pusty słownik na wyniki
    results = {
        "modelName": [],
        "meanScore": [],
        "meanFitTime": [],
        "meanScoreTime": []}
    # lecimy po modelach i uczymy
    for oneM in modelList:
        tmpOneRes = trainCV(modelList[oneM], x_train, y_train)
        print("{0} mean train score = {1}".format(oneM,(tmpOneRes['meanScore'])))
        results["modelName"].append(oneM)
        results["meanScore"].append(tmpOneRes['meanScore'])
        results["meanFitTime"].append(tmpOneRes['meanFitTime'])
        results["meanScoreTime"].append(tmpOneRes['meanScoreTime'])
        #finally fit on whole train data
        modelList[oneM].fit(x_train, y_train)
    
    # present results on charts
    printResultsCharts(results, figsize=figsize)
    plt.savefig(f'../results/porownanie_modeli_R2_i_czas.png')

regrRealResults = TrainAndPrintResults(regrModels, regrSplit) 
# jeżeli chcesz zbaczyć więćej wynikół to włącz soie je w regrModels

def TestAndPrintResults(modelList, dataset, figsize=(15, 5)):
    """
    funkcja przeprowadzająca trening na liście modeli.
    :param modelList: Lista modeli kompatybilnych z pakietem sklearn
    :param dataset: krotka datasetu po podziale na train i test w postaci (x_train, x_test, y_train, y_test)
    """
    # bierzemy z datasetu dane treningowe
    x_train, x_test, y_train, y_test = dataset
    # pusty słownik na wyniki
    results = {
        "modelName": [],
        "testScore": []
    }
    # lecimy po modelach i uczymy
    for oneM in modelList:
        testScore = modelList[oneM].score(x_test, y_test)
        print("{0} score = {1}".format(oneM,testScore))
        results["modelName"].append(oneM)
        results["testScore"].append(testScore)
        
    printResultsCharts(results, figsize=figsize)
    plt.savefig(f'../results/porownanie_modeli_test_score.png')
    
TestAndPrintResults(regrModels, regrSplit)
