import requests, os, re, wget
from bs4 import BeautifulSoup as soup

def auth():
    site = 'https://yandex.ru'

    session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'
    resp = session.get(site)

    print(f'Status code for {site} is: {resp.status_code}\n')

with requests.Session() as session:
    auth()

# Ответ: Status code for https://google.com is: 200