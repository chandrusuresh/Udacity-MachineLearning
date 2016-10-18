###########################################
# Suppress matplotlib user warnings
# Necessary for newer version of matplotlib
import warnings
warnings.filterwarnings("ignore", category = UserWarning, module = "matplotlib")
###########################################

import matplotlib.pyplot as pl
import numpy as np
import sklearn.learning_curve as curves
from sklearn.tree import DecisionTreeRegressor
from sklearn.cross_validation import ShuffleSplit, train_test_split

# Define the kernel function
def kernel(a, b, param):
    sqdist = np.sum(a**2,1).reshape(-1,1) + np.sum(b**2,1) - 2*np.dot(a, b.T)
    return np.exp(-.5 * (1/param) * sqdist)
	
def GP(Xtrain,Ytrain, Xtest):
	param = 0.1
	K_ss = kernel(Xtest, Xtest, param)
	n = len(Xtest)
	# Apply the kernel function to our training points
	K = kernel(Xtrain, Xtrain, param)
	L = np.linalg.cholesky(K + 0.00005*np.eye(len(Xtrain)))

	# Compute the mean at our test points.
	K_s = kernel(Xtrain, Xtest, param)
	Lk = np.linalg.solve(L, K_s)
	mu = np.dot(Lk.T, np.linalg.solve(L, Ytrain)).reshape((-1,1))

	# Compute the standard deviation so we can plot it
	s2 = np.diag(K_ss) - np.sum(Lk**2, axis=0)
	stdv = np.sqrt(s2)
	# Draw samples from the posterior at our test points.
	L = np.linalg.cholesky(K_ss + 1e-6*np.eye(n) - np.dot(Lk.T, Lk))
	f_post = mu.reshape(-1,1) + np.dot(L, np.random.normal(size=(n,1)))
	
	return f_post, mu, stdv
	
