import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV, cross_val_score, validation_curve
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('data_ML.csv')

def validation_curve_max_depth(df, num_est):
    y = df['Price'].values
    X = df.drop('Price', axis=1).values
    
    
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    
    train_scoreNum, test_scoreNum = validation_curve(
                                    RandomForestRegressor(),
                                    X = X_train, y = y_train, 
                                    param_name = 'max_depth', 
                                    param_range = num_est, cv = 3, verbose=0)
    
    
    train_scores_mean = np.mean(train_scoreNum, axis=1)
    train_scores_std = np.std(train_scoreNum, axis=1)
    test_scores_mean = np.mean(test_scoreNum, axis=1)
    test_scores_std = np.std(test_scoreNum, axis=1)
    plt.figure(figsize=(10,10))
    plt.title("Validation Curve with RandomForest")
    plt.xlabel("max_depth")
    plt.ylabel("Score")
    plt.ylim(0.0, 1.1)
    #plt.fill_between(param_range, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, alpha=0.2, color="r")
    plt.plot(num_est, train_scores_mean, label="Training score",
                 color="r")
    #plt.fill_between(param_range, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std, alpha=0.2, color="g")
    plt.plot(num_est, test_scores_mean, label="Cross-validation score",
                 color="g")
    
    plt.legend(loc="best")
    plt.xticks(num_est)
    #plt.savefig('RF_max_depth_2.png')
    plt.show()

def validation_curve_n_estimators(df, num_est):
    y = df['Price'].values
    X = df.drop('Price', axis=1).values
    
    
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    
    train_scoreNum, test_scoreNum = validation_curve(
                                    RandomForestRegressor(),
                                    X = X_train, y = y_train, 
                                    param_name = 'n_estimators', 
                                    param_range = num_est, cv = 3, verbose=0)
    
    
    train_scores_mean = np.mean(train_scoreNum, axis=1)
    train_scores_std = np.std(train_scoreNum, axis=1)
    test_scores_mean = np.mean(test_scoreNum, axis=1)
    test_scores_std = np.std(test_scoreNum, axis=1)
    plt.figure(figsize=(10,10))
    plt.title("Validation Curve with RandomForest")
    plt.xlabel("n_estimators")
    plt.ylabel("Score")
    plt.ylim(0.0, 1.1)
    #plt.fill_between(param_range, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, alpha=0.2, color="r")
    plt.plot(num_est, train_scores_mean, label="Training score",
                 color="r")
    #plt.fill_between(param_range, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std, alpha=0.2, color="g")
    plt.plot(num_est, test_scores_mean, label="Cross-validation score",
                 color="g")
    
    plt.legend(loc="best")
    plt.xticks(num_est)
    #plt.savefig('RF_max_depth_2.png')
    plt.show()