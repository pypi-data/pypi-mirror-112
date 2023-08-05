import numpy as np
from ._rse import rse

def r2_score(a,b):
  return 1 - rse(a,b)