import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui, expected_conditions
import os, pickle, time, random, logging, platform

#  Logging included

logging.basicConfig(level=logging.INFO, filename='logs.log', format='%(asctime)s :: %(levelname)s :: %(message)s')

"""
Use Chrome profile to save previous session.
"""
options = webdriver.ChromeOptions()
profile_dir = os.path.abspath('chrome_profiles/')
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--headless")
options.add_argument("user-data-dir=" + profile_dir)
if platform.system() == 'Linux':
    # options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path='usr/bin/chromedriver', options=options)  # linux
else:
    driver = webdriver.Chrome(options=options)


# Cookie way of saving session
# def open_cookies(driver):
#     cookies = pickle.load(open("cookies.pkl", "rb"))
#     for cookie in cookies:
#         driver.add_cookie(cookie)
#     return driver
#
#
# def save_cookie(driver):
#     ref_xpath = '/html/body/div[2]/div[1]/div[1]/div/div[3]/div[2]/div/a/span[1]'
#     driver.get('http://egbet.live')
#     wait = ui.WebDriverWait(driver, 30)  # Wait until registration passed
#     wait.until(expected_conditions.presence_of_element_located((By.XPATH, ref_xpath)))
#     pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
#     return driver

def logging(driver):
    driver.get('https://egbet.live')
    try:
        # Registration tab by Xpath
        driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[1]/div[1]/div/div[3]/div[2]/a[2]')
        time.sleep(60)  # 60s for logging
    except expected_conditions.NoSuchElementException:
        pass
    return driver


# if os.path.isfile('cookies.pkl'):
#     driver = open_cookies(driver)
# else:
#     driver = save_cookie(driver)
butn_xpaths = [
    '/html/body/div[2]/div[1]/div[4]/div/aside/div/div[4]/div[2]/div[1]/button',
    '/html/body/div[2]/div[1]/div[4]/div/aside/div/div[5]/div[2]/div[1]/button',
    '/html/body/div[2]/div[1]/div[4]/div/aside/div/div[6]/div[2]/div[1]/button'
]
butn_xpaths *= 2  # create 2 cycles

rand_int = random.choices(
    population=[2, 3, 4, 2],
    weights=[25, 25, 25, 25]
)
error_count = 0
success_count = 0

logging(driver)
while True:

    driver.get('https://egbet.live')
    for butn_xpath in butn_xpaths:
        try:
            wait_post = ui.WebDriverWait(driver, 60 * (5 + rand_int[0]), poll_frequency=60)
            wait_post.until(expected_conditions.element_to_be_clickable((By.XPATH, butn_xpath)))
            real_xpath = butn_xpath
            break
        except selenium.common.exceptions.TimeoutException as error:
            logging.info(f'Waiting TimeoutException occured. Error number: {error_count}\nPath used:{butn_xpath}')

    try:
        butn = driver.find_element(by=By.XPATH, value=real_xpath)
    except selenium.common.exceptions.NoSuchElementException as error:
        error_count += 1
        logging.error(f'NoSuchElementException occured; {real_xpath} used. Error number: {error_count}')
        break
    except NameError:
        logging.error(f'No available xpaths in {butn_xpaths[0:3]}')

    try:
        driver.execute_script("arguments[0].click();", butn)
        logging.info(f'Number of success: {success_count}.')
    except selenium.common.exceptions.ElementClickInterceptedException as error:
        error_count += 1
        logging.exception(f'ElementClickInterceptedException occured; Errorlog: {error}\nError number: {error_count}')

    success_count += 1
    if error_count >= 10 or success_count >= 100:  # If something goes completely wrong.
        break
