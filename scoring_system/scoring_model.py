import os
import math
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
from hh_email.email_sender import create_email
from data_manipulation.data_imputation import get_imputed_data
from scoring_system.score_regressor import train_regression_model


class ScoringSystem:
    def __init__(self, df: pd.DataFrame, weights: list):
        self.weights = weights

        self.INACTIVE_WEIGHT = weights[0]

        self.AVG_REP_WEIGHT = (50 / 100) * weights[1]
        self.REP_CHNG_YEAR_WEIGHT = (2.5 / 100) * weights[1]
        self.REP_CHNG_QTR_WEIGHT = (7.5 / 100) * weights[1]
        self.REP_CHNG_MON_WEIGHT = (10 / 100) * weights[1]
        self.REP_CHNG_WEEK_WEIGHT = (13.5 / 100) * weights[1]
        self.REP_CHNG_DAY_WEIGHT = (16.5 / 100) * weights[1]

        self.QUES_WEIGHT = (20 / 100) * weights[2]
        self.ANS_WEIGHT = (80 / 100) * weights[2]

        self.BRONZE_WEIGHT = (10 / 100) * weights[3]
        self.SILVER_WEIGHT = (35 / 100) * weights[3]
        self.GOLD_WEIGHT = (55 / 100) * weights[3]

        self.df = df

    def fit_transform(self):
        timestamp_now = datetime.now().timestamp()

        self.df['account_duration'] = (timestamp_now - self.df['creation_date'])
        self.df['account_duration'] = self.df['account_duration'].apply(self.convert_to_days)

        self.df['inactive_duration'] = (timestamp_now - self.df['last_access_date'])
        self.df['inactive_duration'] = self.df['inactive_duration'].apply(self.convert_to_days)

        self.df['is_registered'] = self.df['user_type'].apply(lambda ut: 1 if ut == "registered" else 0)

        self.df['accept_rate'].fillna(int(np.mean(self.df['accept_rate'])), inplace=True)

        return self.df.apply(lambda data: self.calculate_score(data['account_duration'],
                                                               data['inactive_duration'],
                                                               data['reputation'],
                                                               data['reputation_change_year'],
                                                               data['reputation_change_quarter'],
                                                               data['reputation_change_month'],
                                                               data['reputation_change_week'],
                                                               data['reputation_change_day'],
                                                               data['questions'],
                                                               data['answers'],
                                                               data['bronze_badges'],
                                                               data['silver_badges'],
                                                               data['gold_badges']), axis=1)

    def calculate_score(self, account_duration, inactive_duration, rep, rep_year, rep_qtr, rep_mon, rep_week, rep_day,
                        ques, ans, bb, sb, gb):
        rep_score = (rep / account_duration) * self.AVG_REP_WEIGHT

        inact_score = (1 / inactive_duration) * self.INACTIVE_WEIGHT

        y_c = (rep_year / 365) * self.REP_CHNG_YEAR_WEIGHT
        q_c = (rep_qtr / 90) * self.REP_CHNG_QTR_WEIGHT
        m_c = (rep_mon / 30) * self.REP_CHNG_MON_WEIGHT
        w_c = (rep_week / 7) * self.REP_CHNG_WEEK_WEIGHT
        d_c = (rep_day / 1) * self.REP_CHNG_DAY_WEIGHT

        rep_chng_score = y_c + q_c + m_c + w_c + d_c

        ques_ans_score = (ques * self.QUES_WEIGHT) + (ans * self.ANS_WEIGHT)

        medal_score = (bb * self.BRONZE_WEIGHT) + (sb * self.SILVER_WEIGHT) + (gb * self.GOLD_WEIGHT)

        return (rep_score + inact_score + rep_chng_score + ques_ans_score + medal_score) / np.sum(self.weights)

    @staticmethod
    def convert_to_days(time_in_milis):
        return math.ceil(time_in_milis / 86400)


def generate_scores():
    dataframe = get_imputed_data()
    scoring_system = ScoringSystem(dataframe, [5, 40, 25, 30])
    dataframe['score'] = scoring_system.fit_transform()

    return dataframe


def get_top_users(user_count):
    users_list = list()

    dataframe = generate_scores().sort_values(by='score', ascending=False)
    prev_selected_candidates = dataframe[dataframe['selected'] == 1]

    use_regression_model = False
    if len(prev_selected_candidates) > 50:
        train_regression_model(prev_selected_candidates)
        use_regression_model = True

    if use_regression_model:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, f"./Regression_Model/regression-model.pkl")

        with open(file_path, 'rb') as file:
            model = pickle.load(file)

        selected_users = dataframe[dataframe['selected'] == 0]
        iterator = selected_users.iterrows()

        while user_count > 0:
            current = None
            try:
                current = next(iterator)
            except Exception as e:
                print(e)

            if current:
                values = current[1][['account_duration', 'inactive_duration', 'accept_rate', 'score']]
                values = values.values.reshape(-1, 4)

                result = model.predict(values)[0]

                if result:
                    users_list.append({
                        'display_name': str(selected_users.loc[current[0], 'display_name']),
                        'account_id': int(selected_users.loc[current[0], 'account_id']),
                        'user_id': int(selected_users.loc[current[0], 'user_id']),
                        'score': int(selected_users.loc[current[0], 'score']),
                        'email_id': create_email(str(selected_users.loc[current[0], 'display_name']))
                    })

                    user_count -= 1

                    print("User accepted by the model.")
                else:
                    print("User rejected by the model.")
    else:
        dataframe = dataframe[dataframe['selected'] == 0]
        selected_users = dataframe[['display_name', 'account_id', 'user_id', 'score']].head(user_count)

        for index in selected_users.index:
            try:
                users_list.append({
                    'display_name': str(selected_users.loc[index, 'display_name']),
                    'account_id': int(selected_users.loc[index, 'account_id']),
                    'user_id': int(selected_users.loc[index, 'user_id']),
                    'score': int(selected_users.loc[index, 'score']),
                    'email_id': create_email(str(selected_users.loc[index, 'display_name']))
                })
            except KeyError as e:
                print(e)

    return users_list


if __name__ == '__main__':
    top_users = get_top_users(5)

    for user in top_users:
        print(user)
