from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


driver = webdriver.Chrome()
driver.get("https://www.mvideo.ru/")

assert 'М.Видео - интернет-магазин цифровой и бытовой техники и электроники,' \
       ' низкие цены, большой каталог, отзывы. - Москва' in driver.title


db_names, db_links, db_prices, db_discounts = [], [], [], []

# кол-во элементов в блоке для цикла
count = driver.find_elements_by_class_name('accessories-product-list')[1]
lis = count.find_elements_by_tag_name('li')

pads = driver.find_elements_by_xpath('//div[contains(@data-init,"ajax-category-carousel")]')

pad = None

for _ in pads:
    if 'Хиты продаж' in _.text:
        pad = _
        break

action = ActionChains(driver)

for i in range(0, len(lis)+1):
    button = pad.find_element_by_class_name('sel-hits-button-next')
    button.location_once_scrolled_into_view

    action.move_to_element(button)
    action.perform()

    names = driver.find_elements_by_tag_name('h4')[:4]
    links = driver.find_elements_by_class_name('sel-product-tile-title')[:4]
    prices = driver.find_elements_by_class_name('c-pdp-price__current')[:4]
    discounts = driver.find_elements_by_class_name('c-pdp-price__discount')[:4]

    for name in names:
        db_names.append(name.get_attribute('title'))

    for link in links:
        db_links.append(link.get_attribute('href'))

    for price in prices:
        db_prices.append(int(price.text.replace(' ', '')[:-1]))

    for discount in discounts:
         try:
             db_discounts.append(int(discount.text.replace(' ', '')[1:]))
         except:
             db_discounts.append(0)

    button.send_keys(Keys.ENTER)

driver.quit()