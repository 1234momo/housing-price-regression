import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns

from sklearn.model_selection import StratifiedShuffleSplit
from pandas.plotting import scatter_matrix


housing_data = pd.read_csv('./csv/housing.csv')
print(housing_data.head(5))
print(housing_data.info())

# Display histogram for all 10 features including the y-column
housing_data.hist(bins=50, figsize=(15,15))

# Discretization of continuous feature to perform stratified sampling technique
housing_data['median_income_cat'] = np.ceil(housing_data['median_income'] / 1.5)
housing_data['median_income_cat'].where(housing_data['median_income_cat'] < 5, 5.0, inplace=True)

# Stratified Sampling Technique
stratified_split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

for train_index, test_index in stratified_split.split(housing_data, housing_data['median_income_cat']):
	strat_train_set = housing_data.loc[train_index]
	strat_test_set = housing_data.loc[test_index]

# Removing the median income category from training and test datasets
strat_train_set.drop(['median_income_cat'], axis=1, inplace=True)
strat_test_set.drop(['median_income_cat'], axis=1, inplace=True)

# Creating a copy of the training data set and visualizing with scatter plot
housing_data = strat_train_set.copy()
#housing_data.plot(kind='scatter', x='longitude', y='latitude', alpha=0.5, s=housing_data['population']/30, 
#					c=housing_data['median_house_value'], cmap=plt.get_cmap('jet'), zorder=1, label='Population',
#						colorbar=True, figsize=(15,7))					
plt.legend()


# Using scatter_matrix method to discover correlation amongst all attributes
#attributes = ['median_house_value', 'median_income', 'total_rooms', 'housing_median_age']
#scatter_matrix(housing_data[attributes], figsize=(12, 8))

# Seeing correlation of 'medial house value' with other columns (Pearson's Correlation Coefficient)
corr_matrix = housing_data.corr()
print(corr_matrix['median_house_value'].sort_values(ascending=False))
sns.pairplot(housing_data[['median_house_value', 'median_income', 'total_rooms', 'housing_median_age']])

# Seeing correlation between median house value and the median house income
housing_data.plot(kind='scatter', x='median_income', y='median_house_value', alpha=0.1, figsize=(8,5))


plt.show()
