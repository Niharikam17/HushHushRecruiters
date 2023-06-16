import time
from selenium import webdriver
from database.util import add_profile_urls
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from database.util import get_unfinished_job_profiles


def execute():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get("https://www.google.com/")
    time.sleep(2)

    accept_btn = driver.find_element(By.ID, 'L2AGLb')
    accept_btn.click()
    time.sleep(2)

    job_profiles = get_unfinished_job_profiles()

    for job_profile in job_profiles:
        try:
            driver.get("https://www.google.com/")
            search_query = driver.find_element(By.NAME, 'q')
            search_query.send_keys(job_profile[3])
            search_query.send_keys(webdriver.Keys.RETURN)

            stack_overflow_urls = driver.find_elements(By.CSS_SELECTOR, '.yuRUbf a')
            stack_overflow_urls = [url.get_attribute('href') for url in stack_overflow_urls
                                   if "translate.google.com" not in url.get_attribute('href')]
            if stack_overflow_urls:
                add_profile_urls(stack_overflow_urls, job_profile[0])
            else:
                break
        except Exception as e:
            print(e)


if __name__ == '__main__':
    execute()
