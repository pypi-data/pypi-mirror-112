class Union:
    def __init__(self, *steps):
        self.steps = steps

    def fit(self, X, y=None):
        for key, step in self.steps:
            getattr(step, 'fit')(X, y)
        return self

    def transform(self, X):
        result = []
        for key, step in self.steps:
            result.append(getattr(step, 'transform')(X))
        return result

    def fit_transform(self, X, y=None):
        result = []
        for key, step in self.steps:
            result.append(getattr(step, 'fit_transform')(X, y))
        return result


class Pipeline:
    def __init__(self, *steps):
        self.steps = steps

    def fit(self, X, y=None):
        result = X
        for key, step in self.steps[:-1]:
            result = getattr(step, 'fit_transform')(result, y)
        getattr(self.steps[-1][1], 'fit')(result, y)
        return self

    def transform(self, X):
        result = X
        for key, step in self.steps:
            result = getattr(step, 'transform')(result)
        return result

    def predict(self, X):
        result = X
        for key, step in self.steps[:-1]:
            result = getattr(step, 'transform')(result)
        return getattr(self.steps[-1][1], 'predict')(result)

    def fit_predict(self, X, y):
        result = X
        for key, step in self.steps[:-1]:
            result = getattr(step, 'fit_transform')(result, y)
        return getattr(self.steps[-1][1], 'fit_predict')(result)

    def fit_transform(self, X, y=None):
        result = X
        for key, step in self.steps:
            result = getattr(step, 'fit_transform')(result, y)
        return result
