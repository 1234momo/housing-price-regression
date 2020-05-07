import numpy as np
import pandas as pd
import math

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor 
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error

from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt
import seaborn as sns
from preprocessing import *
sns.set()

# Casting from numpy.ndarray to Pandas DataFrame 
# data = pd.DataFrame(housing_data_prepared)
# Split data into training and validation set
# X = data.drop('zestimate/tax_value', axis=1)
# y = data['zestimate/tax_value']

X_train, X_test, y_train, y_test = train_test_split(housing_data_prepared, housing_labels, random_state=42, test_size=0.4)

# PCA to remove noise and reduce overfitting
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
pca = PCA(n_components=7)
X_train = pca.fit_transform(X_train)
X_test = pca.transform(X_test)

# ~~~ Fit Linear Regression and log performance ~~~ #
linear_regression = LinearRegression()
linear_regression.fit(X_train, y_train)

print('\nLINEAR REGRESSION')
print('Training Score: {}'.format(linear_regression.score(X_train, y_train)))
print('Test Score: {}'.format(linear_regression.score(X_test, y_test)))

y_pred = linear_regression.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = math.sqrt(mse)
print('RMSE: {}'.format(rmse))

# ~~~ Linear Regrssion with standardized and polynomial features ~~~ #
linear_steps = [
	('scalar', StandardScaler()),
	('poly', PolynomialFeatures(degree=2)),
	('model', LinearRegression())
]
linear_pipeline = Pipeline(linear_steps)
linear_pipeline.fit(X_train, y_train)
print('\nLINEAR AFTER STANDARDIZING & POLYNOMIAL FEATURES')
print('Training Score: {}'.format(linear_pipeline.score(X_train, y_train)))
print('Test Score: {}'.format(linear_pipeline.score(X_test, y_test)))


# ~~~ Fit Random Forest Regression and log performance ~~~ #
random_forest = RandomForestRegressor() 
random_forest.fit(X_train, y_train)
print('\nRANDOM FOREST REGRESSION')
print('Training Score: {}'.format(random_forest.score(X_train, y_train)))
print('Test Score: {}'.format(random_forest.score(X_test, y_test)))

y_pred = random_forest.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = math.sqrt(mse)
print('RMSE: {}'.format(rmse))

# ~~~ Random Forest Regression with standardized and polynomial features ~~~ #
forest_steps = [
	('scaler', StandardScaler()),
	('poly', PolynomialFeatures(degree=2)),
	('model', Ridge(alpha=10, fit_intercept=True))
]
forest_pipeline = Pipeline(forest_steps)
forest_pipeline.fit(X_train, y_train)
print('\nFOREST AFTER STANDARDIZING & POLYNOMIAL FEATURES')
print('Training Score: {}'.format(forest_pipeline.score(X_train, y_train)))
print('Test Score: {}'.format(forest_pipeline.score(X_test, y_test)))

# ~~~ L2 Regularization (ridge) ~~~ #
ridge_steps = [
	('scalar', StandardScaler()),
	('poly', PolynomialFeatures(degree=2)),
	('model', Ridge(alpha=10, fit_intercept=True))
]
ridge_pipeline = Pipeline(ridge_steps)
ridge_pipeline.fit(X_train, y_train)
print('\nL2 REGULARIZATION')
print('Training Score: {}'.format(ridge_pipeline.score(X_train, y_train)))
print('Test Score: {}'.format(ridge_pipeline.score(X_test, y_test)))


# ~~~ L1 Regularization (lasso) ~~~ #
lasso_steps = [
	('scaler', StandardScaler()),
	('poly', PolynomialFeatures(degree=2)),
	('model', Lasso(alpha=0.3, fit_intercept=True))
]
lasso_pipeline = Pipeline(lasso_steps)
lasso_pipeline.fit(X_train, y_train)
print('\nL1 REGULARIZATION')
print('Training Score: {}'.format(lasso_pipeline.score(X_train, y_train)))
print('Test Score: {}'.format(lasso_pipeline.score(X_test, y_test)))

