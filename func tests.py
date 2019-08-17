import pandas as pd
import requests
from bs4 import BeautifulSoup as soup
from pprint import pprint

vacancy = 'программист'
language = 'python'
city = 'moskva.'
salary = '?st=1'


def get_vac_names():

    vac_name = soup(resp.text, 'lxml').find_all('a', {'data-category': "sourceAway"})

    vac_names = []

    for i in range(0, len(vac_name)):
        vac_names.append(vac_name[i].getText())

    return vac_names


# def get_salaries():
#     vac_salary = soup(resp.text, 'lxml').find_all('/h2/span/b')
#
#     vac_salaries = []
#
#     for i in range(0, len(vac_salary)):
#         vac_salaries.append(vac_salary[i].get_text())
#
#     return vac_salaries

with requests.Session() as session:

    session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'

    url = f'https://{city}gorodrabot.ru/{vacancy}_{language}{salary}'
    resp = session.get(url)

    print(f'gorodrabot.ru status code is: {resp.status_code}')

    vac_salary = soup(resp.text, 'lxml')

    pprint(vac_salary.h2.span.b.getText())


