import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from preprocessing import *

print('dataset size initially :', len(housing_data_prepared))
pca = PCA(n_components=12)
pca.fit_transform(housing_data_prepared)
pca.transform(housing_data_prepared)
print('reduced dataset size: ', len(housing_data_prepared))

print(pca.explained_variance_ratio_)
print(pca.explained_variance_ratio_.cumsum())
