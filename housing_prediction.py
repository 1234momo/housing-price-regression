import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score

from preprocessing import *
#from house_estimate import * 

# Linear Regression with K-fold cross-validation (across 10 folds)
linear_regression = LinearRegression()
linear_regression_scores = cross_val_score(linear_regression, housing_data_prepared, housing_labels, scoring='neg_mean_squared_error', cv=10)
# Computing RMSE to get rid of negative score values
linear_rmse_scores = np.sqrt(-linear_regression_scores)
print('LINEAR REGRESSION PERFORMANCE ACROSS 10 FOLDS:')
print('Mean:\t\t\t ', linear_rmse_scores.mean(), '\nStandard Deviation:\t', linear_rmse_scores.std())


# Decision-Tree Regression with k-fold cross-validation
decision_tree = DecisionTreeRegressor()
decision_tree_scores = cross_val_score(decision_tree, housing_data_prepared, housing_labels, scoring='neg_mean_squared_error', cv=10)
# Computing the RMSE to get rid of negative score values
decision_rmse_scores = np.sqrt(-decision_tree_scores)
print('DECISION-TREE REGRESSION PERFORMANCE ACROSS 10 FOLDS:')
print('Mean:\t\t\t ', decision_rmse_scores.mean(), '\nStandard Deviation:\t', decision_rmse_scores.std())


# Random Forest Regression
forest_regression = RandomForestRegressor()
forest_regression.fit(housing_data_prepared, housing_labels)

RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=None,
				min_impurity_decrease=0.0, min_impurity_split=None, min_samples_leaf=1, 
				min_samples_split=2, min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=None, 
				oob_score=False, random_state=None, verbose=0, warm_start=False)

forest_regression_scores = cross_val_score(forest_regression, housing_data_prepared, housing_labels, scoring='neg_mean_squared_error', cv=10)
forest_rmse_scores = np.sqrt(-forest_regression_scores)
print('RANDOM-FOREST REGRESSION PERFORMANCE(MAX-DEPTH=5):')
print('Mean:\t\t\t ', forest_rmse_scores.mean(), '\nStandard Deviation:\t', forest_rmse_scores.std())
