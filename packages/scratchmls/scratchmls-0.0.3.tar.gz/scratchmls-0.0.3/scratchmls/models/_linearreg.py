import numpy as np

class LinearRegression:

    def __init__(self, learning_rate=0.01, n_iters=1000):
        self.learning_rate = learning_rate
        self.n_iters = n_iters
        self.theta = None
        self.bias = None

    def fit(self, X, y):
        X =  (X - X.mean(axis =0))/X.std(axis=0)
        rows = X.shape[0]
        cols = X.shape[1]
        X = np.append(np.ones((rows, 1)), X, axis=1)
        try:
          y = y.values.reshape(rows, 1)
        except Exception:
          y = y
        self.theta = np.zeros((cols+1,1))
        self.bias = 0
        m = len(y)
        for _ in range(self.n_iters):
            h = np.dot(X,self.theta) + self.bias
            error = (h - y)
            self.theta = self.theta - self.learning_rate*((1/m)*np.dot(X.T,error))
            self.bias = self.bias - self.learning_rate*((1/m)*np.sum(error))

    def predict(self, X):
        X =  (X - X.mean(axis =0))/X.std(axis=0)
        rows = X.shape[0]
        X = np.append(np.ones((rows, 1)), X, axis=1)
        y_pred = np.dot(X,self.theta) + self.bias
        return y_pred