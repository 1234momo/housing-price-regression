import numpy as np

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score

from preprocessing import *
# from house_estimate import * 

# Linear Regression with K-fold cross-validation (across 10 folds)
linear_regression = LinearRegression()
# linear_regression_scores = cross_val_score(linear_regression, housing_data_prepared, housing_labels, scoring='neg_mean_squared_error', cv=10)
linear_regression_scores = cross_val_score(linear_regression, housing_data_prepared, housing_labels, scoring='neg_mean_squared_error', cv=10)
# Computing RMSE to get rid of negative score values
linear_rmse_scores = np.sqrt(-linear_regression_scores)
print('LINEAR REGRESSION PERFORMANCE ACROSS 10 FOLDS: (RMSE)')
print('Mean:\t\t\t ', linear_rmse_scores.mean(), '\nStandard Deviation:\t', linear_rmse_scores.std())
# print('LINEAR REGRESSION PERFORMANCE ACROSS 10 FOLDS: (ACCURACY)')
# print('Mean:\t\t\t ', linear_regression_scores.mean(), '\nStandard Deviation:\t', linear_regression_scores.std())


# KNN Regression with K-fold cross-validation
knn_regression = KNeighborsRegressor()
knn_regression_scores = cross_val_score(knn_regression, housing_data_prepared, housing_labels, scoring='neg_mean_squared_error', cv=10)
# knn_regression_scores = cross_val_score(knn_regression, housing_data_prepared, housing_labels, cv=10)
knn_rmse_scores = np.sqrt(-knn_regression_scores)
print('KNN REGRESSION PERFORMANCE ACROSS 10 FOLDS (RMSE)')
print('Mean:\t\t\t ', knn_rmse_scores.mean(), '\nStandard Deviation:\t', knn_rmse_scores.std())
# print('KNN REGRESSION PERFORMANCE ACROSS 10 FOLDS (ACCURACY)')
# print('Mean:\t\t\t ', knn_regression_scores.mean(), '\nStandard Deviation:\t', knn_regression_scores.std())


# Support Vector Regression (SVR) with K-fold cross-validation
sv_regression = SVR()
svr_scores = cross_val_score(sv_regression, housing_data_prepared, housing_labels, scoring='neg_mean_squared_error', cv=10)
# svr_scores = cross_val_score(sv_regression, housing_data_prepared, housing_labels, cv=10)
svr_rmse_scores = np.sqrt(-svr_scores)
print('SUPPORT VECTOR REGRESSION PERFORMANCE ACROSS 10 FOLDS (RMSE)')
print('Mean:\t\t\t ', svr_rmse_scores.mean(), '\nStandard Deviation:\t', svr_rmse_scores.std())
# print('SUPPORT VECTOR REGRESSION PERFORMANCE ACROSS 10 FOLDS (ACCURACY)')
# print('Mean:\t\t\t ', svr_scores.mean(), '\nStandard Deviation:\t', svr_scores.std())


# Decision-Tree Regression with k-fold cross-validation
decision_tree = DecisionTreeRegressor()
decision_tree_scores = cross_val_score(decision_tree, housing_data_prepared, housing_labels, scoring='neg_mean_squared_error', cv=10)
# decision_tree_scores = cross_val_score(decision_tree, housing_data_prepared, housing_labels, cv=10)
# Computing the RMSE to get rid of negative score values
decision_rmse_scores = np.sqrt(-decision_tree_scores)
print('DECISION-TREE REGRESSION PERFORMANCE ACROSS 10 FOLDS: (RMSE)')
print('Mean:\t\t\t ', decision_rmse_scores.mean(), '\nStandard Deviation:\t', decision_rmse_scores.std())
# print('DECISION-TREE REGRESSION PERFORMANCE ACROSS 10 FOLDS: (ACCURACY)')
# print('Mean:\t\t\t ', decision_tree_scores.mean(), '\nStandard Deviation:\t', decision_tree_scores.std())


# Random Forest Regression
forest_regression = RandomForestRegressor()
forest_regression.fit(housing_data_prepared, housing_labels)

RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=None,
				min_impurity_decrease=0.0, min_impurity_split=None, min_samples_leaf=1, 
				min_samples_split=2, min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=None, 
				oob_score=False, random_state=None, verbose=0, warm_start=False)

forest_regression_scores = cross_val_score(forest_regression, housing_data_prepared, housing_labels, scoring='neg_mean_squared_error', cv=10)
# forest_regression_scores = cross_val_score(forest_regression, housing_data_prepared, housing_labels, cv=10)
forest_rmse_scores = np.sqrt(-forest_regression_scores)
print('RANDOM-FOREST REGRESSION PERFORMANCE ACROSS 10 FOLDS: (RMSE)')
print('Mean:\t\t\t ', forest_rmse_scores.mean(), '\nStandard Deviation:\t', forest_rmse_scores.std())
# print('RANDOM-FOREST REGRESSION PERFORMANCE ACROSS 10 FOLDS: (ACCURACY)')
# print('Mean:\t\t\t ', forest_regression_scores.mean(), '\nStandard Deviation:\t', forest_regression_scores.std())
