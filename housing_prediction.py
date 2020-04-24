import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score

from preprocessing import *


# Linear Regression with K-fold cross-validation (across 10 folds)
linear_regression = LinearRegression()
scores = cross_val_score(linear_regression, housing_data_prepared, housing_labels, scoring='neg_mean_squared_error', cv=10)

# Computing RMSE to get rid of negative score values
rmse_scores = np.sqrt(-scores)

print('Mean:\t\t ', rmse_scores.mean(), '\nStandard Deviation:', rmse_scores.std())
