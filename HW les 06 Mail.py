from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import time

# mongo клиент
client = MongoClient('mongodb://127.0.0.1:27017')
gmail = client['gmail']
db = gmail.gmail

lgn = None
psw = None

driver = webdriver.Chrome()
driver.get("https://gmail.com")

# Ф-ция ожидания элемента
def Wait(CSS, driver=driver,):
    return wait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, CSS)))

# Передаем логин
login = driver.find_element_by_css_selector('#identifierId').send_keys(lgn)

# next button click
driver.find_element_by_css_selector('#identifierNext').click()

# Передаем в пароль
password = Wait('#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input').send_keys(psw)

# next button click
Wait('#passwordNext').click()

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

    title = Wait('h2.hP').text

    sender = Wait('span.go').text[1:-1]

    date = Wait('span.g3').get_attribute('title')

    date, time_ = date.split(',')

    text = Wait('.ii.gt').text

    db.insert_one({'title': title,
                   'sender': sender,
                   'date': date,
                   'time': time_,
                   'body': text})

    driver.back()
    time.sleep(2)

driver.quit()

for i in db.find({}):
    print(i)

# print(f'{title}\n')
# print(f'{sender}\n')
# print(f'{date}\n')
# print(f'{time_}\n')
# print(f'{text}\n')