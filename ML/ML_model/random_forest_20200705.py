import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from datetime import datetime
from csv import DictWriter
import os.path

# Dataset
data = pd.read_csv('data.csv')

# Target
y = df['Price'].values

# Data
X = df.drop('Price', axis=1).values
