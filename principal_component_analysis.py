import pandas as pd
import numpy as np

def get_eigenvalues(dataframe):
	# calculate the mean of each column (feature)
	mean = np.mean(dataframe.T, axis=1)

	# center columns by subtracting column means
	centered_matrix = (dataframe - mean)
	
	# calculate covariance matrix of centered matrix
	covariance_matrix = np.cov(centered_matrix.T)
	
	# using numpy's eig function to compute eigenvector and eigenvalues of covariance matrix
	eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)
	print(f'COMPUTED EIGENVALUES:\n {eigenvalues}')
	
	# computing variance of each PC and accumulating a total variance
	variances = []
	total_variance = 0
	for eigenvalue in eigenvalues:
		variance = eigenvalue / (len(dataframe) - 1)
		variances.append(variance)
		total_variance += variance

	principal_components = {}
	for index, variance in enumerate(variances):
		variance_ratio = variance / total_variance
		principal_components[index] = variance_ratio

	# sorting the dictionary in descending order by variance ratio
	sorted_pcs = dict(sorted(principal_components.items(), reverse=True, key=lambda x: abs(x[1])))
	
	print('\n')
	# outputting the results
	for key in sorted_pcs:
		print(f'Principal Component #{key}: {sorted_pcs[key]}')
