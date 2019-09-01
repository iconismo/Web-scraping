from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient

lgn = None
psw = None

#
driver = webdriver.Chrome()
driver.get("https://gmail.com")

# Передаем логин
login = driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys(lgn)
driver.find_element_by_xpath('//*[@id="identifierNext"]/span/span').click()

#  Передаем в пароль
password = wait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'))).send_keys(psw)

# password.send_keys(psw)
driver.find_element_by_xpath('//*[@id="passwordNext"]').click()

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
trs = letters.find_elements_by_tag_name('tr')

#  В цикле кликаем на каждое письмо и заходим в него.
for tr in trs[:10]:
    tr.click()

    title = wait(driver, 20).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, '#\:17o'))) # True

    #  Элемент невидимый, невозможно его как-либо зафиксировать или выбрать. С остальными элементами
    # которые нужны - тоже самое.
    break


    # title = driver.find_element_by_xpath('//*[@id=":1"]/div/div[3]/div/table/tr/td[1]/div[2]/div[1]/div[2]/div[1]').text

    # sender = driver.find_element_by_xpath('//*[@id=":177"]/div[1]/div[2]/div[1]/table/tbody/'
    #                                       'tr[1]/td[1]/table/tbody/tr/td/h3/span[1]/span[1]').get_attribute('email')

    # date = driver.find_element_by_xpath('//*[@id=":1s4"]').text
    # body = driver.find_element_by_xpath('//*[@id="m_7877200117708243263bodyCell"]').text

print(f'{title}\n')
    # print(f'{sender}\n')
    # print(f'{date}\n')
    # print(f'{body}\n')



# driver.quit()