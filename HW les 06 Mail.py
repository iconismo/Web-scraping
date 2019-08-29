from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient

lgn = None
psw = None

driver = webdriver.Chrome()
driver.get("https://gmail.com")

login = driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys(lgn)
driver.find_element_by_xpath('//*[@id="identifierNext"]/span/span').click()


password = wait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))

password.send_keys(psw)
driver.find_element_by_xpath('//*[@id="passwordNext"]/span/span').click()

# cats = wait(driver, 5).until(
#     EC.presence_of_element_located((By.XPATH, '//*[@id=":lw"]/div/div[1]')))
#
# cats.click()

search = wait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="gs_lc50"]/input[1]')))

# promos = search.send_keys('category:promotions')
# scope = driver.find_element_by_xpath('//*[@id="aso_search_form_anchor"]/button[4]/svg')

# action = ActionChains(driver)
#
# find = action.move_to_element(search)
# find.send_keys('category:promotions')
# find.send_keys(Keys.ENTER)
# action.perform()

# driver.quit()