import unittest
import numpy as np
import scratchmls
from scratchmls.models import LinearRegression
from scratchmls.metrics import r2_score

class Tests(unittest.TestCase):
    def test_linear1(self):
        #Input values
        xs = np.array([[73,67,43],[91,88,64],[87,134,58],[102,43,37],[69,96,70]], dtype='float32')
        #Actual target values
        ys = np.array([[56,70],[81,101],[119,133],[22,37],[103,119]], dtype='float32')

        clf = LinearRegression(learning_rate=0.01,n_iters=1000)
        clf.fit(xs,ys)
        ys_pred = clf.predict(xs)
        j = r2_score(ys,ys_pred)
        self.assertGreaterEqual(j,0.8)

    def test_linear2(self):
        #Input values
        xs = np.array([[73,67,43],[91,88,64],[87,134,58],[102,43,37],[69,96,70]], dtype='float32')
        #Actual target values
        ys = np.array([[56,70],[81,101],[119,133],[22,37],[103,119]], dtype='float32')

        clf = LinearRegression(learning_rate=0.01,n_iters=1000)
        clf.fit(xs,ys)
        ys_pred = clf.predict(xs)
        j = r2_score(ys,ys_pred)
        self.assertLessEqual(j,1.0)

if __name__=="__main__":
    unittest.main()