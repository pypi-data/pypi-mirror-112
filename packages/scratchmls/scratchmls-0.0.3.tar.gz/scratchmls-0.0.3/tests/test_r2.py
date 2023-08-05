import unittest
import numpy as np
import scratchmls
from scratchmls.metrics import r2_score

class Tests(unittest.TestCase):
    def test_r2_1(self):
        #Actual target values
        ys = np.array([[56,70],[81,101],[119,133],[22,37],[103,119]], dtype='float32')
        # predicted values
        ys_pred = np.array([[ 56.59964446,69.7410952 ],[ 82.76655889,101.16619189],[118.26863192,132.69443989],[ 21.2080857,37.12363473],[102.15878436,119.27293304]], dtype='float32')
        j = r2_score(ys,ys_pred)
        self.assertGreaterEqual(j,0.8)

    def test_r2_2(self):
        #Actual target values
        ys = np.array([[56,70],[81,101],[119,133],[22,37],[103,119]], dtype='float32')
        # predicted values
        ys_pred = np.array([[ 56.59964446,69.7410952 ],[ 82.76655889,101.16619189],[118.26863192,132.69443989],[ 21.2080857,37.12363473],[102.15878436,119.27293304]], dtype='float32')
        j = r2_score(ys,ys_pred)
        self.assertLessEqual(j,1.0)

if __name__=="__main__":
    unittest.main()
    