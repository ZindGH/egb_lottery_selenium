import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui, expected_conditions
import os, pickle, time, random, logging

#  Logging included

logging.basicConfig(level=logging.INFO, filename='logs.log', format='%(asctime)s :: %(levelname)s :: %(message)s')

"""
Use Chrome profile to save previous session.
"""
options = webdriver.ChromeOptions()
profile_dir = os.path.abspath('chrome_profiles/')
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox") # linux only
options.add_argument("--headless")
options.add_argument("user-data-dir=" + profile_dir)
driver = webdriver.Chrome(options=options)


# Cookie way of saving session
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
butn_xpath = [
    '/html/body/div[2]/div[1]/div[4]/div/aside/div/div[5]/div[2]/div[1]/button',
    '/html/body/div[2]/div[1]/div[4]/div/aside/div/div[6]/div[2]/div[1]/button'
]

rand_int = random.choices(
    population=[2, 3, 4, 5, 11],
    weights=[30, 30, 30, 5, 5]
)
error_count = 0
success_count = 0
while True:
    logging.info(f'Number of success: {success_count}.')
    driver.get('https://egbet.live')
    try:
        wait_post = ui.WebDriverWait(driver, 60 * (30 + rand_int[0]), poll_frequency=120)
        wait_post.until(expected_conditions.element_to_be_clickable((By.XPATH, butn_xpath[0])))
    except selenium.common.exceptions.TimeoutException as error:
        error_count += 1
        logging.exception(f'Waiting TimeoutException occured. Error number: {error_count}\n{error}')
    try:
        butn = driver.find_element(by=By.XPATH, value=butn_xpath[0])
    except selenium.common.exceptions.NoSuchElementException as error:
        error_count += 1
        logging.info(f'NoSuchElementException occured; xpath[1] used. Error number: {error_count}')
        butn = driver.find_element(by=By.XPATH, value=butn_xpath[1])
    try:
        driver.execute_script("arguments[0].click();", butn)
    except selenium.common.exceptions.ElementClickInterceptedException as error:
        error_count += 1
        logging.exception(f'ElementClickInterceptedException occured; Errorlog: {error}\nError number: {error_count}')

    success_count += 1
    if error_count >= 10 or success_count >= 100:  # If something goes completely wrong.
        break
