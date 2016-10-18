import numpy as np
import matplotlib.pyplot as plt
import math
import visuals as vs

#%matplotlib inline

# Train data

Xtrain = np.array([-4, -3, -2, -1, 1]).reshape(5,1)
Ytrain = np.sin(Xtrain)

# Plot
plt.plot(Xtrain,Ytrain,'r')
plt.show()

n = 50
x = np.linspace(-5, 5, n).reshape(-1,1)
y = np.zeros(np.size(x))
# Plot
plt.plot(x,y,'ro')
plt.plot(Xtrain,Ytrain)
plt.show()

y_prediction,mu,stdv = vs.GP(Xtrain,Ytrain,x)
plt.plot(Xtrain, Ytrain, 'bs', ms=8)
plt.plot(x, y_prediction)
#plt.plot(x,mu-2*stdv,'g')
#plt.plot(x,mu+2*stdv,'g')

mu = mu.flat
stdv = stdv.flat
plt.plot(x, mu, 'r--', lw=2)

plt.gca().fill_between(x, (mu-2*stdv).flat, (mu+2*stdv).flat)#, color="#dddddd")
##plt.plot(Xtest, mu, 'r--', lw=2)
plt.axis([-5, 5, -3, 3])
#plt.title('Three samples from the GP posterior')
plt.show()