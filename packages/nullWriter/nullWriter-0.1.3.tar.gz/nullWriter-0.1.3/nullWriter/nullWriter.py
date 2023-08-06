import numpy as np
from sklearn.base import ClassifierMixin
class NullRegressor(ClassifierMixin):
    def fit(self, X=None, y=None):
        # The prediction will always just be the mean of y
        self.y_bar_ = "Hello World!"
    def predict(self, X=None):
        # Give back the mean of y, in the same
        # length as the number of X observations
        return "Hello World!"#np.ones(X.shape[0]) * self.y_bar_
