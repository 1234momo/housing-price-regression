import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

housing_data = pd.read_csv('./csv/housing.csv')
print(housing_data.head(5))
print(housing_data.info()) 

housing_data.hist(bins=50, figsize=(15,15))
plt.show()
