#
# In this and the following exercises, you'll be adding train test splits to the data
# to see how it changes the performance of each classifier
#
# The code provided will load the Titanic dataset like you did in project 0, then train
# a decision tree (the method you used in your project) and a Bayesian classifier (as
# discussed in the introduction videos). You don't need to worry about how these work for
# now. 
#
# What you do need to do is import a train/test split, train the classifiers on the
# training data, and store the resulting accuracy scores in the dictionary provided.

import numpy as np
import pandas as pd

# Load the dataset
X = pd.read_csv('titanic_data.csv')
# Limit to numeric data
X = X._get_numeric_data()
# Separate the labels
y = X['Survived']
# Remove labels from the inputs, and age due to missing data
del X['Age'], X['Survived']

from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

# TODO: split the data into training and testing sets,
# using the standard settings for train_test_split.
# Then, train and test the classifiers with your newly split data instead of X and y.
from sklearn.cross_validation import train_test_split
feature_train, feature_test, label_train, label_test = train_test_split(X,y)


# The decision tree classifier
clf1 = DecisionTreeClassifier()
clf1.fit(feature_train,label_train)
print "Decision Tree has accuracy: ",accuracy_score(clf1.predict(feature_test),label_test)
# The naive Bayes classifier

clf2 = GaussianNB()
clf2.fit(feature_train,label_train)
print "GaussianNB has accuracy: ",accuracy_score(clf2.predict(feature_test),label_test)

#score

score = { 
 "Naive Bayes Score": accuracy_score(clf2.predict(feature_test),label_test), 
 "Decision Tree Score": accuracy_score(clf1.predict(feature_test),label_test)
}

#Consufion matrix
from sklearn.metrics import confusion_matrix
confusions = {
 "Naive Bayes": confusion_matrix(clf2.predict(feature_test), label_test),
 "Decision Tree": confusion_matrix(clf1.predict(feature_test), label_test)
}

print confusions

# Precision and recall
from sklearn.metrics import recall_score as recall
from sklearn.metrics import precision_score as precision
results = {
  "Naive Bayes Recall": recall(clf2.predict(feature_test),label_test),
  "Naive Bayes Precision": precision(clf2.predict(feature_test),label_test),
  "Decision Tree Recall": recall(clf1.predict(feature_test),label_test),
  "Decision Tree Precision": precision(clf1.predict(feature_test),label_test)
}

print results

# Naive Bayes
from sklearn.metrics import f1_score
F1_scores = {
 "Naive Bayes": f1_score(clf2.predict(feature_test),label_test),
 "Decision Tree": f1_score(clf1.predict(feature_test),label_test)
}
print F1_scores