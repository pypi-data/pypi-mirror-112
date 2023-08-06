import abc


class Transformer(abc.ABC):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        raise NotImplementedError

    def fit_transform(self, X, y=None):
        return self.fit(X, y).transform(X)


class Estimator(abc.ABC):
    def fit(self, X, y):
        return self

    def predict_log_proba(self, X):
        raise NotImplementedError

    def predict_proba(self, X):
        raise NotImplementedError

    def predict(self, X):
        raise NotImplementedError

    def fit_predict(self, X, y):
        return self.fit(X, y).predict(X)


class FunctionTransformer(Transformer):
    def __init__(self, func):
        super().__init__()
        self._transform = func

    def transform(self, X):
        return self._transform(X)


def transformer(func):
    return FunctionTransformer(func)
