import os
import pickle
from data_manipulation.data_cleaning import get_refined_user_data
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor


def create_and_save_questions_predicting_model(dataframe):
    model = GradientBoostingRegressor(loss='absolute_error', learning_rate=0.15)

    X = dataframe[['joindate', 'reputation', 'goldbadges', 'silverbadges', 'bronzebadges']].values
    y = dataframe[['questions']].values.ravel()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=90)

    model.fit(X_train, y_train)

    predicted = model.predict(X_test)

    print(f"Questions Model's 'Mean Absolute Error' is: {mean_absolute_error(y_test, predicted)}")

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "./Trained_Models/questions-model.pkl")

    with open(file_path, "wb") as file:
        pickle.dump(model, file)


def create_and_save_answers_predicting_model(dataframe):
    model = GradientBoostingRegressor(loss='absolute_error', learning_rate=0.1)

    X = dataframe[['joindate', 'reputation', 'goldbadges', 'silverbadges', 'bronzebadges']].values
    y = dataframe[['answers']].values.ravel()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=90)

    model.fit(X_train, y_train)

    predicted = model.predict(X_test)

    print(f"Answers Model's 'Mean Absolute Error' is: {mean_absolute_error(y_test, predicted)}")

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "./Trained_Models/answers-model.pkl")

    with open(file_path, "wb") as file:
        pickle.dump(model, file)


if __name__ == '__main__':
    df = get_refined_user_data()

    create_and_save_questions_predicting_model(df)
    create_and_save_answers_predicting_model(df)
