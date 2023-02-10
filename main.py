from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui, expected_conditions
import os
import pickle
import time

# options = webdriver.ChromeOptions()
profile_dir = os.path.abspath('chrome_profiles/')
# print(profile_dir)
# options.add_argument(f'user-data-dir={profile_dir}'

options = webdriver.ChromeOptions()
profile_dir = os.path.abspath('chrome_profile/')
options.add_argument("user-data-dir=" + profile_dir)
driver = webdriver.Chrome(options=options)

def open_cookies(driver):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    return driver
def save_cookie(driver):
    ref_xpath = '/html/body/div[2]/div[1]/div[1]/div/div[3]/div[2]/div/a/span[1]'
    driver.get('http://egbet.live')
    wait = ui.WebDriverWait(driver, 30)  # Wait until registration passed
    wait.until(expected_conditions.presence_of_element_located((By.XPATH, ref_xpath)))
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    return driver

# if os.path.isfile('cookies.pkl'):
#     driver = open_cookies(driver)
# else:
#     driver = save_cookie(driver)
time.sleep(10)


# print(lottery_button.is_enabled())