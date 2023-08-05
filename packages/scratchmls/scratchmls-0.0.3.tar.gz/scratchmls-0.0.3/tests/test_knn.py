# import unittest
# import os,sys,inspect

# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0,parentdir)

# import numpy as np
# import scratchml
# from scratchml.models import KNN

# class Tests(unittest.TestCase):
#     def test_knn1(self):


# search for small data for testing

# from sklearn import datasets
# from sklearn.model_selection import train_test_split
# from scratchml.models import KNN
# from scratchml.metrics import accuracy

# iris = datasets.load_iris()
# X,y = iris.data, iris.target

# # train-test split
# X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=1234)

# # instantiating our classifier
# clf = KNN(k=5)
# clf.fit(X_train,y_train)

# predictions = clf.predict(X_test)

# print("Accuracy : {:.4f}".format(accuracy(y_test, predictions)))

