import time
from selenium import webdriver
from database.util import add_user_data
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from database.util import get_unfinished_profile_urls
from webdriver_manager.chrome import ChromeDriverManager


def extract_data_from_webpage(driver, xpath):
    data = str()

    try:
        element = driver.find_element(By.XPATH, xpath)
        data = element.text.strip()
    except Exception as e:
        print(e)

    return data


def execute():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    profile_urls = get_unfinished_profile_urls()

    for profile_url_id, url, _ in profile_urls:
        driver.get(url)

        try:
            user_name = extract_data_from_webpage(driver, '//*[@id="mainbar-full"]/div[1]/div[1]/div/div/div[1]')

            join_date = extract_data_from_webpage(driver, '//*[@id="mainbar-full"]/div[1]/div[1]/div/ul/li['
                                                          '1]/div/div[2]/span')

            last_online = extract_data_from_webpage(driver, '//*[@id="mainbar-full"]/div[1]/div[1]/div/ul/li['
                                                            '2]/div/div[2]')

            reputation = extract_data_from_webpage(driver, '//*[@id="stats"]/div[2]/div/div[1]/div')

            reached = extract_data_from_webpage(driver, '//*[@id="stats"]/div[2]/div/div[2]/div')

            answers = extract_data_from_webpage(driver, '//*[@id="stats"]/div[2]/div/div[3]/div')

            questions = extract_data_from_webpage(driver, '//*[@id="stats"]/div[2]/div/div[4]/div')

            gold_badges = extract_data_from_webpage(driver, '//*[@id="main-content"]/div/div[2]/div/div[3]/div['
                                                            '2]/div[1]/div/div[1]/div[2]/div[1]')

            silver_badges = extract_data_from_webpage(driver, '//*[@id="main-content"]/div/div[2]/div/div[3]/div['
                                                              '2]/div[2]/div/div[1]/div[2]/div[1]')

            bronze_badges = extract_data_from_webpage(driver, '//*[@id="main-content"]/div/div[2]/div/div[3]/div['
                                                              '2]/div[3]/div/div[1]/div[2]/div[1]')

            user_data = dict()
            user_data['user_name'] = user_name
            user_data['join_date'] = join_date
            user_data['last_online'] = last_online
            user_data['reputation'] = reputation
            user_data['reached'] = reached
            user_data['answers'] = answers
            user_data['questions'] = questions
            user_data['gold_badges'] = gold_badges
            user_data['silver_badges'] = silver_badges
            user_data['bronze_badges'] = bronze_badges
            user_data['extra_info'] = '{}'

            add_user_data(profile_url_id, user_data)
        except Exception as e:
            print(e)

        time.sleep(1)


if __name__ == '__main__':
    execute()
