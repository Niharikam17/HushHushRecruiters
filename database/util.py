import json
import random
from hh_email.email_sender import create_email
from database.connector import get_database_connection


def add_job_profile(index, c, jp, url, finished):
    database = get_database_connection()
    cursor = database.cursor()

    sql = "INSERT INTO job_profiles (`id`, `city`, `jobprofile`, `url`,`finished`)" \
          "VALUES (%s, %s, %s, %s, %s)"

    val = (index, c, jp, url, finished)

    cursor.execute(sql, val)

    database.commit()


def get_unfinished_job_profiles():
    database = get_database_connection()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM job_profiles WHERE finished = 0")

    return cursor.fetchall()


def add_profile_urls(stack_overflow_urls, job_profile_id):
    database = get_database_connection()
    cursor = database.cursor()

    for stack_overflow_url in stack_overflow_urls:
        sql = "INSERT INTO profile_urls (`id`, `url`, `finished`) VALUES (%s, %s, %s)"

        try:
            index = random.randint(100000, 999999)
            val = (index, stack_overflow_url, False)
            cursor.execute(sql, val)
            database.commit()
        except Exception as e:
            print("Entered into Index Error: ", e)
            index = random.randint(100000, 999999)
            val = (index, stack_overflow_url, False)
            cursor.execute(sql, val)
            database.commit()

    cursor_two = database.cursor()
    sql = "UPDATE job_profiles SET `finished` = %s WHERE (`id` = %s)"
    val = (1, job_profile_id)
    cursor_two.execute(sql, val)
    database.commit()


def get_unfinished_profile_urls():
    database = get_database_connection()
    cursor = database.cursor()

    cursor.execute("SELECT * FROM profile_urls WHERE finished = 0")

    return cursor.fetchall()


def add_user_data(profile_url_id, user_data):
    database = get_database_connection()
    cursor = database.cursor()

    sql = "INSERT INTO `hush_hush`.`user_raw_data` (`id`, `username`, `joindate`, `lastonline`, `reputation`, " \
          "`reached`, `answers`, `questions`, `goldbadges`, `silverbadges`, `bronzebadges`, `extrainfo`) VALUES (" \
          "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    try:
        index = random.randint(100000, 999999)

        val = (index, user_data['user_name'], user_data['join_date'], user_data['last_online'], user_data['reputation'],
               user_data['reached'], user_data['answers'], user_data['questions'], user_data['gold_badges'],
               user_data['silver_badges'], user_data['bronze_badges'], user_data['extra_info'])

        cursor.execute(sql, val)

        database.commit()
    except Exception as e:
        print("Entered into Index Error: ", e)

        index = random.randint(100000, 999999)

        val = (index, user_data['user_name'], user_data['join_date'], user_data['last_online'], user_data['reputation'],
               user_data['reached'], user_data['answers'], user_data['questions'], user_data['gold_badges'],
               user_data['silver_badges'], user_data['bronze_badges'], user_data['extra_info'])

        cursor.execute(sql, val)

        database.commit()

    cursor_two = database.cursor()
    sql = "UPDATE profile_urls SET `finished` = %s WHERE (`id` = %s)"
    val = (1, profile_url_id)
    cursor_two.execute(sql, val)
    database.commit()


def add_user_data_from_se(user_data):
    database = get_database_connection()
    cursor = database.cursor()

    sql = "INSERT INTO `hush_hush`.`stackexchange_users` (`account_id`, `user_id`, `is_employee`, " \
          "`last_modified_date`, `last_access_date`, `reputation_change_year`, `reputation_change_quarter`, " \
          "`reputation_change_month`, `reputation_change_week`, `reputation_change_day`, `reputation`, " \
          "`creation_date`, `user_type`, `accept_rate`, `location`, `website_url`, `link`, `display_name`, " \
          "`bronze_badges`, `silver_badges`, `gold_badges`, `collectives`) VALUES (%s, %s, %s, %s, %s, %s, %s," \
          "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

    val = (user_data.get('account_id'), user_data.get('user_id'), user_data.get('is_employee'),
           user_data.get('last_modified_date'), user_data.get('last_access_date'),
           user_data.get('reputation_change_year'), user_data.get('reputation_change_quarter'),
           user_data.get('reputation_change_month'), user_data.get('reputation_change_week'),
           user_data.get('reputation_change_day'), user_data.get('reputation'), user_data.get('creation_date'),
           user_data.get('user_type'), user_data.get('accept_rate'), user_data.get('location'),
           user_data.get('website_url'), user_data.get('link'), user_data.get('display_name'),
           user_data.get("badge_counts")['bronze'], user_data.get("badge_counts")['silver'],
           user_data.get("badge_counts")['gold'], json.dumps(user_data.get("collectives")))

    cursor.execute(sql, val)

    database.commit()


def update_user_selection_status(account_id, selected):
    database = get_database_connection()
    cursor = database.cursor()

    sql = "UPDATE `stackexchange_users` SET `selected` = %s WHERE (`account_id` = %s);"

    val = (selected, account_id)

    cursor.execute(sql, val)

    database.commit()


def update_user_exam_status(account_id, attempted, passed):
    database = get_database_connection()
    cursor = database.cursor()

    sql = "UPDATE `stackexchange_users` SET `attempted` = %s, `passed` = %s WHERE (`account_id` = %s);"

    val = (attempted, passed, account_id)

    cursor.execute(sql, val)

    database.commit()


def get_user_email_id(account_id):
    database = get_database_connection()
    cursor = database.cursor()

    cursor.execute(f"SELECT display_name FROM hush_hush.stackexchange_users where account_id = {account_id};")

    result = cursor.fetchone()

    return create_email(result[0])


if __name__ == '__main__':
    pass
