from sklearn.base import BaseEstimator, TransformerMixin


class CustomModelTransformer(BaseEstimator, TransformerMixin):
    # Class Constructor
    def __init__(self, model=None):
        """
        model: the previously trained model to transform the data, e.g. a sklearn Gaussian Mixture Model
        """
        self.model = model

    # Return self, nothing else to do here
    def fit(self, X, y=None):
        return self

    # Custom transform method we wrote that creates aformentioned features
    def transform(self, X, y=None):
        data = X.copy()
        print('columns:', data.columns)
        transformed_data = self.model.predict(data)
        return transformed_data.astype('int')
