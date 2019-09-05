from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
import time

from pymongo import MongoClient

lgn = None
psw = None

driver = webdriver.Chrome()
driver.get("https://gmail.com")

# Передаем логин
login = driver.find_element_by_css_selector('#identifierId').send_keys(lgn)

# next button click
driver.find_element_by_css_selector('#identifierNext').click()

# Передаем в пароль
password = wait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#password > div.aCsJod.oJeWuf > '
                                                     'div > div.Xb9hP > input'))).send_keys(psw)
# next button click
wait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#passwordNext'))).click()

# Ищем поисковую строку в ящике по xpath
search = wait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="gs_lc50"]/input[1]')))

#  Передаем поисковой запрос в строку: Категория:Промоакции
search.send_keys('category:promotions')
search.send_keys(Keys.ENTER)

# Блок с списком писем
letters = wait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id=":nw"]/tbody')))

# Список писем
trs = letters.find_elements_by_css_selector('tr.zA')

#  В цикле кликаем на каждое письмо и заходим в него.
for tr in trs[:10]:
    tr.click()

    title = wait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.hP'))).text

    sender = wait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'span.go'))).text[1:-1]

    date = wait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'span.g3'))).get_attribute('title')

    date, time_ = date.split(',')

    text = wait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.ii.gt'))).text

    driver.back()
    time.sleep(2)

driver.quit()

# TODO Доделать добавление в Монго, остальное сделано.



# print(f'{title}\n')
# print(f'{sender}\n')
# print(f'{date}\n')
# print(f'{time_}\n')
# print(f'{text}\n')



# driver.quit()