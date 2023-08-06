from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.mixture import GaussianMixture
import numpy as np


class GaussianMixtureTransformer(BaseEstimator, TransformerMixin):
    # Class Constructor
    def __init__(self, n_components=[3]):
        """
        :param n_components: list of integers for each of the columns to be transformed
        """
        self.n_components = n_components

    # Return self, nothing else to do here
    def fit(self, X, y=None):
        return self

    # Custom transform method we wrote that creates aformentioned features
    def transform(self, X, y=None):
        data = X.copy()
        n_rows, n_cols = data.values.shape
        transformed_data = np.zeros(data.values.shape)
        print('columns:', data.columns)
        for i in range(n_cols):
            gmm = GaussianMixture(n_components=self.n_components[i], random_state=0).fit(data[:, i])

            print({i: mean for i, mean in enumerate(gmm.means_)})
            transformed_data[:, i] = gmm.predict(data[:, i])
        return transformed_data.astype('int')
