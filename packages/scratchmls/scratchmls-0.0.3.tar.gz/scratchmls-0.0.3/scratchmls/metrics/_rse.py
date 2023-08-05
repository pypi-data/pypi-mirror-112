import numpy as np 

def rse(a,b):
  return float(np.sum((a-b)**2)) / float(np.sum((a-np.mean(a))**2))
