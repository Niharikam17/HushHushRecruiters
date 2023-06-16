import os
import pickle
import warnings
from sklearn.svm import LinearSVC

warnings.filterwarnings('ignore')


def train_regression_model(dataframe):
    model = LinearSVC()

    X = dataframe[['account_duration', 'inactive_duration', 'accept_rate', 'score']].values
    y = dataframe[['attempted']].values.ravel()

    model.fit(X, y)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "./Regression_Model/regression-model.pkl")

    with open(file_path, "wb") as file:
        pickle.dump(model, file)
