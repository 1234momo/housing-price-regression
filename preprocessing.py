import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns

from sklearn.model_selection import StratifiedShuffleSplit
from pandas.plotting import scatter_matrix
from sklearn.impute import SimpleImputer

# for eigenvalue analysis
from principal_component_analysis import *

# Pipeline imports
from pipeline import *
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import FeatureUnion
from sklearn.preprocessing import LabelEncoder, LabelBinarizer, MultiLabelBinarizer


"""
	Various data visualization/KDD techniques to deeply understand the data
	Also includes various data preprocessing techniques and compilation of a pipeline
"""


pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

# Loading dataset
# housing_data = pd.read_csv('./csv/housing.csv')
# housing_data = pd.read_csv('./csv/housing copy.csv')
housing_data = pd.read_csv('./csv/combined_data.csv')
# housing_data = pd.read_csv('combined_data_zip_city.csv')
print('Dataset initially:')
print(housing_data.head(5), '\n')
print(housing_data.info()) 


# Display histogram for all 10 features including the y-column
housing_data.hist(bins=50, figsize=(15,15))

# Discretization of continuous feature to perform stratified sampling technique (continuous features can't extract a mode for stratisfied sampling)
housing_data['median_income_cat'] = np.ceil(housing_data['median_income'] / 1.5)
housing_data['median_income_cat'].where(housing_data['median_income_cat'] < 5, 5.0, inplace=True)
# print('median_income_cat\n', housing_data['median_income_cat'])
# print('unique vals in cat\n', np.unique(housing_data['median_income_cat']))

# STRATIFIED SAMPLING TECHNIQUE
stratified_split = StratifiedShuffleSplit(n_splits=3, test_size=0.2, random_state=42)

for train_index, test_index in stratified_split.split(housing_data, housing_data['median_income_cat']):
	strat_train_set = housing_data.loc[train_index]
	strat_test_set = housing_data.loc[test_index]

# Removing the median income category from training and test datasets
strat_train_set.drop(['median_income_cat'], axis=1, inplace=True)
strat_test_set.drop(['median_income_cat'], axis=1, inplace=True)

# Creating a copy of the training data set and visualizing with scatter plot
housing_data = strat_train_set.copy()
housing_data.plot(kind='scatter', x='longitude', y='latitude', alpha=0.5, s=housing_data['population']/30, 
				  c=housing_data['median_house_value'], cmap=plt.get_cmap('jet'), zorder=1, label='Population',
				  colorbar=True, figsize=(15,7))					
plt.legend()


# Using scatter_matrix method to discover correlation amongst all attributes
attributes = ['median_house_value', 'median_income', 'longitude', 'latitude']
scatter_matrix(housing_data[attributes], figsize=(12, 8))
sns.pairplot(housing_data[['median_house_value', 'median_income', 'longitude', 'latitude']])

# Seeing correlation of 'medial house value' with other columns (Pearson's Correlation Coefficient)
corr_matrix = housing_data.corr()
print('\nCorrelation Matrix before Data Preprocessing')
print(corr_matrix['median_house_value'].sort_values(ascending=False))


# Seeing correlation between median house value and the median house income
#housing_data.plot(kind='scatter', x='median_income', y='median_house_value', alpha=0.1, figsize=(8,5))

# DATA PREPROCESSING: correcting 'total_rooms', 'total_bedroom', and 'population' from units of per block to per household
housing_data['rooms_per_household'] = housing_data['total_rooms'] / housing_data['households']
housing_data['bedrooms_per_room'] = housing_data['total_bedrooms'] / housing_data['total_rooms']
housing_data['population_per_household'] = housing_data['population'] / housing_data['households']
#print(housing_data.head(3))

# Seeing correlation of 'medial house value' with other columns again (Pearson's correlation coefficient)
corr_matrix = housing_data.corr()
print('\nCorrelation Matrix after Data Preprocessing')
print(corr_matrix['zestimate/tax_value'].sort_values(ascending=False))

# Creating a training and testing set
# housing_data = strat_train_set.drop('median_house_value', axis=1)
# housing_labels = strat_train_set['median_house_value'].copy()
housing_data = strat_train_set.drop('zestimate/tax_value', axis=1)
housing_labels = strat_train_set['zestimate/tax_value'].copy()

# DATA PREPROCESSING: imputing missing values in total_bedrooms column with median value
# imputer = SimpleImputer(strategy='median')
housing_num = housing_data.drop('ocean_proximity', axis=1) 
housing_num = housing_num.drop('address', axis=1) 
# housing_num = housing_num.drop('city', axis=1) 
#print(housing_num.head())


# Defining the Preprocessing Pipeline
numerical_features = list(housing_num)
categorical_features = ['ocean_proximity']
multilabel_categorical_features = ['address']
# multilabel_categorical_features = ['city']

feature_adder = FeatureAdder(add_bedrooms_per_room = False)
housing_extra_features = feature_adder.transform(housing_data.values)

# Adding componenets/classes to numerical pipeline
numerical_pipeline = Pipeline([
	('selector', DataFrameSelector(numerical_features)),
	('imputer', SimpleImputer(strategy='median')),
	('feature_adder', FeatureAdder()),
	('std_scaler', StandardScaler())
])

# Adding componenets/classes to categorical pipeline
categorical_pipeline = Pipeline([
	('selector', DataFrameSelector(categorical_features)),
	('label_binarizer', MyLabelBinarizer())
])

# Address is multi-output, so needs its own special pipeline
multilabel_categorical_pipeline = Pipeline([
	('selector', DataFrameSelector(multilabel_categorical_features)),
	('multilabel_binarizer', MyMultiLabelBinarizer())
])

# Full pipeline
full_pipeline = FeatureUnion(transformer_list=[
	('num_pipeline', numerical_pipeline),
	('cat_pipeline', categorical_pipeline),
	('multilabel_cat_pipeline', multilabel_categorical_pipeline)
])

housing_data_prepared = full_pipeline.fit_transform(housing_data)
print('\nDataframe after Preprocessing Pipeline:\n', housing_data_prepared)





"""
# PCA Eigenvalue Analysis
encoder = LabelEncoder()
imputer = SimpleImputer(strategy='median')

housing_data['ocean_proximity'] = encoder.fit_transform(housing_data['ocean_proximity'])
housing_data['address'] = encoder.fit_transform(housing_data['address'])
housing_data = pd.DataFrame(imputer.fit_transform(housing_data))

# Using PCA to view eigenvalues in descending order of all columns (variance)
print('\nPCA after Data Preprocessing')
get_eigenvalues(housing_data)
"""
#plt.show()
