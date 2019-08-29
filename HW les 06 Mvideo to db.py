from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient


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


# MongoDB insertion

client = MongoClient('mongodb://127.0.0.1:27017')
mvideo = client['mvideo']
db = mvideo.mvideo

if len(db_names) == len(db_links) == len(db_prices) == len(db_discounts):
    for i in range(0, len(db_names)):

        db.insert_one({'name': db_names[i],
                       'price': db_prices[i],
                       'discount': db_discounts[i],
                       'link': db_links[i]})

for i in db.find({}):
    print(i)


# Вывод (Убрал id):

# {'name': 'Ноутбук Acer Aspire 3 A315-21-64A8 NX.GNVER.065', 'price': 19990, 'discount': 5000, 'link': 'https://www.mvideo.ru/products/noutbuk-acer-aspire-3-a315-21-64a8-nx-gnver-065-30042330'}
# {'name': 'Стиральная машина узкая Hotpoint-Ariston RST 702 ST S', 'price': 19990, 'discount': 4000, 'link': 'https://www.mvideo.ru/products/stiralnaya-mashina-uzkaya-hotpoint-ariston-rst-702-st-s-20032713'}
# {'name': 'Смартфон Samsung Galaxy S10E Оникс', 'price': 49990, 'discount': 7000, 'link': 'https://www.mvideo.ru/products/smartfon-samsung-galaxy-s10e-oniks-30042525'}
# {'name': 'Телевизор Samsung UE43RU7200U', 'price': 34990, 'discount': 2000, 'link': 'https://www.mvideo.ru/products/televizor-samsung-ue43ru7200u-10021429'}
# {'name': 'Ноутбук Acer Aspire 3 A315-21-64A8 NX.GNVER.065', 'price': 19990, 'discount': 5000, 'link': 'https://www.mvideo.ru/products/noutbuk-acer-aspire-3-a315-21-64a8-nx-gnver-065-30042330'}
# {'name': 'Стиральная машина узкая Hotpoint-Ariston RST 702 ST S', 'price': 19990, 'discount': 4000, 'link': 'https://www.mvideo.ru/products/stiralnaya-mashina-uzkaya-hotpoint-ariston-rst-702-st-s-20032713'}
# {'name': 'Смартфон Samsung Galaxy S10E Оникс', 'price': 49990, 'discount': 7000, 'link': 'https://www.mvideo.ru/products/smartfon-samsung-galaxy-s10e-oniks-30042525'}
# {'name': 'Телевизор Samsung UE43RU7200U', 'price': 34990, 'discount': 2000, 'link': 'https://www.mvideo.ru/products/televizor-samsung-ue43ru7200u-10021429'}
# {'name': 'Ноутбук Lenovo IdeaPad S145-15IWL (81MV00HHRU)', 'price': 24990, 'discount': 5000, 'link': 'https://www.mvideo.ru/products/noutbuk-lenovo-ideapad-s145-15iwl-81mv00hhru-30045074'}
# {'name': 'Музыкальный центр LG XBOOM DM5660K', 'price': 11990, 'discount': 4000, 'link': 'https://www.mvideo.ru/products/muzykalnyi-centr-lg-xboom-dm5660k-10010951'}
# {'name': 'Смартфон Huawei P Smart Z Sapphire Blue (STK-LX1)', 'price': 16990, 'discount': 3000, 'link': 'https://www.mvideo.ru/products/smartfon-huawei-p-smart-z-sapphire-blue-stk-lx1-30043655'}
# {'name': 'Холодильник Samsung RB37J5000WW', 'price': 39990, 'discount': 7000, 'link': 'https://www.mvideo.ru/products/holodilnik-samsung-rb37j5000ww-20039363'}
# {'name': 'Ноутбук Lenovo IdeaPad S145-15IWL (81MV00HHRU)', 'price': 24990, 'discount': 5000, 'link': 'https://www.mvideo.ru/products/noutbuk-lenovo-ideapad-s145-15iwl-81mv00hhru-30045074'}
# {'name': 'Музыкальный центр LG XBOOM DM5660K', 'price': 11990, 'discount': 4000, 'link': 'https://www.mvideo.ru/products/muzykalnyi-centr-lg-xboom-dm5660k-10010951'}
# {'name': 'Смартфон Huawei P Smart Z Sapphire Blue (STK-LX1)', 'price': 16990, 'discount': 3000, 'link': 'https://www.mvideo.ru/products/smartfon-huawei-p-smart-z-sapphire-blue-stk-lx1-30043655'}
# {'name': 'Холодильник Samsung RB37J5000WW', 'price': 39990, 'discount': 7000, 'link': 'https://www.mvideo.ru/products/holodilnik-samsung-rb37j5000ww-20039363'}
# {'name': 'Электрический самокат Tribe Himba Black', 'price': 27990, 'discount': 5000, 'link': 'https://www.mvideo.ru/products/elektricheskii-samokat-tribe-himba-black-10021403'}
# {'name': 'Посудомоечная машина (45 см) Midea MFD45S320W', 'price': 17990, 'discount': 3000, 'link': 'https://www.mvideo.ru/products/posudomoechnaya-mashina-45-sm-midea-mfd45s320w-20040178'}
# {'name': 'Наушники для Apple Apple AirPods w/Wireless Charg.Case MRXJ2', 'price': 16990, 'discount': 5000, 'link': 'https://www.mvideo.ru/products/naushniki-dlya-apple-apple-airpods-w-wireless-charg-case-mrxj2-50126637'}
# {'name': 'Кофемашина капсульного типа Nespresso DeLonghi ENV 155. S', 'price': 14990, 'discount': 0, 'link': 'https://www.mvideo.ru/products/kofemashina-kapsulnogo-tipa-nespresso-delonghi-env-155-s-20062488'}
