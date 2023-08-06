from hyperopt import Trials, fmin, space_eval
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold

from mxdesign.base import Estimator


def k_fold_iterator(n_splits=5):
    kf = KFold(n_splits=n_splits, random_state=None, shuffle=False)

    def iter(*arrays):
        X = arrays[0]
        for train_index, test_index in kf.split(X):
            X_train, X_test = X[train_index], X[test_index]
            yield X_train, X_test

    return iter


class CrossValidator:
    def __init__(self, estimator, scoring=accuracy_score, iterator=k_fold_iterator(k=5)):
        self.estimator = estimator
        self.scoring = scoring
        self.iterator = iterator

    def validate(self, X, y):
        results = []
        for X_train, X_test, y_train, y_test in self.iterator(X, y):
            model = self.estimator.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            score = self.scoring(y_test, y_pred)
            results.append(score)
        return results


class ModelSelection(Estimator):
    def __init__(self, cv, param_space, strategy, max_evals=25, verbose=False, show_progressbar=False):
        self.cv = cv
        self.param_space = param_space
        self.strategy = strategy
        self.max_evals = max_evals
        self.verbose = verbose
        self.show_progressbar = show_progressbar
        self.fit_X_y_ = None
        self.trials_ = None
        self.model_ = None

    def objective(self, params):
        for attr, value in params:
            setattr(self.cv.estimator, attr, value)
        return self.cv.validate(**self.fit_X_y_)

    def fit(self, X, y):
        self.fit_X_y_ = dict(X=X, y=y)
        self.trials_ = Trials()
        best = fmin(
            self.objective,
            self.param_space,
            algo=self.strategy,
            max_evals=self.max_evals,
            trials=self.trials_,
            verbose=self.verbose,
            show_progressbar=self.show_progressbar,
        )
        best_params = space_eval(self.param_space, best)
        estimator = self.cv.estimator
        for attr, value in best_params:
            setattr(estimator, attr, value)
        self.model_ = estimator.fit(**self.fit_X_y_)
        return self

    def predict_log_proba(self, X):
        return self.model_.predict_log_proba(X)

    def predict_proba(self, X):
        return self.model_.predict_proba(X)

    def predict(self, X):
        return self.model_.predict(X)
