import pandas as pd
import requests
from bs4 import BeautifulSoup as soup
from pprint import pprint


class Scrapper():

    def __init__(self, vacancy, language, city, salary):
        self.vacancy = vacancy
        self.language = language
        self.city = city
        self.salary = salary

    def auth(self, vacancy, language, city, salary):

        session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'

        url = f'https://{city}gorodrabot.ru/{vacancy}_{language}{salary}'
        resp = session.get(url)

        print(f'gorodrabot.ru status code is: {resp.status_code}')



with requests.Session() as session:

    vacancy = 'программист'
    language = 'python'
    city = 'moskva.'
    salary = '?st=1'

    scrapper = Scrapper(vacancy, language, city, salary)
    scrapper.auth(vacancy, language, city, salary)

