import pandas as pd
import numpy as np
import requests, re
import time as timer
from datetime import datetime, date, time, timedelta
from bs4 import BeautifulSoup as soup
from pprint import pprint


def get_vac_names(resp_text):
    div = str(resp_text.find_all('div', {'class': ['clearfix vacancy premium ',
                                                   'clearfix vacancy']}))
    h2 = soup(div, 'lxml').find_all('h2')
    vac_names = []

    for i in h2:
        vac_names.append(i.a.getText())

    return vac_names


def time_ago(resp_text):
    span = resp_text.find_all('span', {'class': 'date'})
    time_ago = []

    for i in range(0, len(span)):
        time = span[i].find(text=True, recursive=False).replace('  ', '')[1:]
        time_ago.append(time)

    return time_ago


def post_datetime(time_ago, resp_text):
    time_ago = time_ago(resp_text)
    date_time = []

    for i in time_ago:
        now = datetime.now()

        if not i:
            date_time.append(0)
        else:
            num, rest = i.split(' ', 1)

            if rest.startswith('ч'):
                date_time.append(now - timedelta(hours=int(num)))
            elif rest.startswith('д'):
                date_time.append(now - timedelta(days=int(num)))
            elif rest.startswith('н'):
                date_time.append(now - timedelta(weeks=int(num)))
            elif rest.startswith('м'):
                date_time.append(now - timedelta(weeks=int(num) * 4))
            else:
                date_time.append(0)

    return date_time


def get_salaries(resp_text):
    h2 = resp_text.find_all('h2')
    salaries = []

    for i in h2:
        sal = re.findall(mask, i.b.getText())
        salaries.append(''.join(sal))

    return salaries


def get_links(resp_text):
    div = str(soup(resp.text, 'lxml').find_all('div', {'class': ['clearfix vacancy premium ',
                                                                 'clearfix vacancy']}))
    h2 = str(soup(div, 'lxml').find_all('h2'))

    a = list(soup(h2, 'lxml').find_all('a'))

    vac_links = []

    for i in range(0, len(a)):
        vac_links.append('http://gorodrabot.ru' + a[i].get('href'))

    return vac_links


def get_id(get_links):
    vac_links = get_links
    ids = []

    for i in vac_links:
        ids.append(int(i[29:38]))

    return ids


# ! TODO

### Переделать без множественного парсинга в функциях
# (get_links, hirer, get_comp и тд, где возможно)


def hirer(resp_text):
    div = str(soup(resp.text, 'lxml').find_all('div', {'class': ['clearfix vacancy premium ',
                                                                 'clearfix vacancy']}))
    h2 = str(soup(div, 'lxml').find_all('h2'))

    a = list(soup(h2, 'lxml').find_all('a'))
    hirers = []

    for i in range(0, len(a)):
        hirers.append(a[i].get('data-action'))

    return hirers


# def get_comp():

#   div = str(soup(resp.text, 'lxml').find_all('div', {'class': ['clearfix vacancy premium ',
#                                                                'clearfix vacancy']}))
#   div = str(soup(div, 'lxml').find_all('div', {'class': 'address'}))

#   span = list(soup(div, 'lxml').find_all('span'))

#   comp = []

#   for i in range(0, len(span)):
#     comp.append(span[i])

#   return comp

# ! TODO

### Доделать вывод названия компаний.

def salary_separator(resp_text):
    ot = []
    do = []
    salaries = get_salaries(resp_text)

    for i in salaries:
        if i.startswith('от'):
            ot.append(int(i[2:]))
            do.append(0)

        elif i.startswith('до'):
            if i.startswith('дог'):
                ot.append(-1)
                do.append(-1)
            else:
                do.append(int(i[2:]))
                ot.append(0)

        else:
            a = i.split('—')

            ot.append(int(a[0]))
            do.append(int(a[1]))

    return ot, do


def temp_df(time_ago, resp_text):
    df = pd.DataFrame({'vacancy': get_vac_names(resp_text),
                       'salary min': salary_separator(resp_text)[0],
                       'salary max': salary_separator(resp_text)[1],
                       'link': get_links(resp_text),
                       'vac_id': get_id(get_links(resp_text)),
                       'from': hirer(resp_text),
                       'datetime': post_datetime(time_ago, resp_text)
                       })

    return df


# url params

mask = '[а-я0-9—]+'
vacancy = 'программист'
language = 'python'
city = 'moskva.'
salary = '?st=1'

# resulting dataframe

result = pd.DataFrame(columns=['vacancy',
                               'salary min',
                               'salary max',
                               'link',
                               'vac_id',
                               'from',
                               'datetime'
                               ])

with requests.Session() as session:
    n = 2

    for i in range(1, n):
        page = f'&p={i}'

        session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'

        url = f'https://{city}gorodrabot.ru/{vacancy}_{language}{salary}{page}'
        resp = session.get(url)

        # timer.sleep(10)

        resp_text = soup(resp.text, 'lxml')

        print(f'gorodrabot.ru status code is: {resp.status_code}\n'
              f'Обработка страницы {i} из {n - 1}\n')

        df = temp_df(time_ago, resp_text)

        result = result.append(df, ignore_index=True)

# result.info()
# result.head(3)

# Добавление записей в MongoDB

from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017')
vacs = client['vacs']
db = vacs.vacs

for i in range(0, result.shape[0]):

    counter = 0 #TODO доделать для отображения кол-ва новых добавленных записей

    row = result.iloc[[i]].to_dict(orient='index')

    db.insert_one({'vacancy': row[i]['vacancy'],
                   'sal_min': row[i]['salary min'],
                   'sal_max': row[i]['salary max'],
                   'link': row[i]['link'],
                   'vac_id': row[i]['vac_id'],
                   'portal': row[i]['from'],
                   'datetime': row[i]['datetime']})

for i in db.find({}):
    print(i)

# Вывод:
# Вывод верный но, чтобы не устраивать свалку - вывел только несколько первых элементов и заменил id, link на Х для экономии места.

# gorodrabot.ru status code is: 200
# Обработка страницы 1 из 1

# {'_id': ObjectId(x), 'vacancy': 'Программист 1C', 'sal_min': 120000, 'sal_max': 150000, 'link': x, 'vac_id': 197954599, 'portal': 'rabota.ru', 'datetime': datetime.datetime(2019, 3, 6, 20, 26, 47, 546000)}
# {'_id': ObjectId(x), 'vacancy': 'Разработчик Backend (Middle)', 'sal_min': 180000, 'sal_max': 250000, 'link':x, 'vac_id': 198182127, 'portal': 'rabota.ru', 'datetime': datetime.datetime(2019, 8, 14, 20, 26, 47, 546000)}
# {'_id': ObjectId(x), 'vacancy': 'Backend-разработчик (python 3)', 'sal_min': 100000, 'sal_max': 200000, 'link': x, 'vac_id': 193786676, 'portal': 'talents.yandex.ru', 'datetime': datetime.datetime(2019, 8, 21, 8, 26, 47, 546000)}
# {'_id': ObjectId(x), 'vacancy': 'Windows-разработчик со знанием JS', 'sal_min': 80000, 'sal_max': 0, 'link': x, 'vac_id': 198424878, 'portal': None, 'datetime': 0}
# {'_id': ObjectId(x), 'vacancy': 'Intelligent R&D Tools Technical Expert', 'sal_min': 300000, 'sal_max': 0, 'link': x, 'vac_id': 196539228, 'portal': 'kellyservices.ru', 'datetime': datetime.datetime(2019, 7, 24, 20, 26, 47, 546000)}
