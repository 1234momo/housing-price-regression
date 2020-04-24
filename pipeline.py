import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelBinarizer
rooms_ix, bedrooms_ix, population_ix, household_ix = 3, 4, 5, 6

"""
	Preprocessing Pipeline with Custom Transformers
		- there are changes
		- we want to play around with out model
		- if input data has changed
		- we want to try different things
"""

# This class adds new features to our pipeline
class FeatureAdder(BaseEstimator, TransformerMixin):
	def __init__(self, add_bedrooms_per_room = True):
		self.add_bedrooms_per_room = add_bedrooms_per_room

	def fit(self, X, y=None): return self

	def transform(self, X, y=None):
		rooms_per_household = X[:, rooms_ix] / X[:, household_ix]
		population_per_household = X[:, population_ix] / X[:, household_ix]
		
		if self.add_bedrooms_per_room:
			bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]
			return np.c_[X, rooms_per_household, population_per_household, bedrooms_per_room]
		else:
			return np.c_[X, rooms_per_household, population_per_household]


# This class allows us to select entire or partial dataframes
# (i.e. we can control which attributes we want in our pipeline)
class DataFrameSelector(BaseEstimator, TransformerMixin):
	def __init__(self, attribute_names):
		self.attribute_names = attribute_names
	
	def fit(self, X, y=None): return self
	
	def transform(self, X): return X[self.attribute_names].values


""" 
	 This class converts categorical data to nominal data by some means
		- text to integers
		- integers to one hot vectors (encoding style: array of all 0's and one 1)
"""
class MyLabelBinarizer(TransformerMixin):
	def __init__(self, *args, **kwargs):
		self.encoder = LabelBinarizer(*args, **kwargs)

	def fit(self, x, y=0):
		self.encoder.fit(x)
		return self
	
	def transform(self, x, y=0): return self.encoder.transform(x)


