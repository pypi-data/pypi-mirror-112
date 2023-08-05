import numpy as np
from collections import Counter

# implementing formula for euclidean distance
def euclidean_distance(x1,x2):
  return np.sqrt(np.sum((x1-x2)**2))

#creating the KNN classifier class
class KNN:
  #setting k = 3 as default value
  def __init__(self,k=3):
    self.k = k
  
  def fit(self,X,y):
    self.X_train = X
    self.y_train = y
  
  def predict(self,X):
    y_pred = [self._predict(x) for x in X]
    return np.array(y_pred)

  def _predict(self,x):
    #distance
    distances = [euclidean_distance(x,x_train) for x_train in self.X_train]
    # k nearest samples
    k_indices = np.argsort(distances)[:self.k]
    final_y_train = np.array(self.y_train)
    k_nearest_labels = [final_y_train[i] for i in k_indices]
    # most common class label
    most_common = Counter(k_nearest_labels).most_common(1)
    return most_common[0][0]