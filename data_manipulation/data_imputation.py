import os
import pickle
from data_manipulation.data_cleaning import get_stack_exchange_data


def impute_column(dataframe, col_name, file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, f"./Trained_Models/{file_name}")

    with open(file_path, 'rb') as file:
        model = pickle.load(file)

    required_cols = dataframe[['creation_date', 'reputation', 'gold_badges', 'silver_badges', 'bronze_badges']].values

    dataframe[col_name] = model.predict(required_cols)
    dataframe[col_name] = dataframe[col_name].astype('int64')

    return dataframe


def get_imputed_data():
    dataframe = get_stack_exchange_data()

    dataframe = impute_column(dataframe, 'questions', 'questions-model.pkl')
    dataframe = impute_column(dataframe, 'answers', 'answers-model.pkl')

    return dataframe


if __name__ == '__main__':
    df = get_imputed_data()
    print(df[['questions', 'answers']].sample(10))
