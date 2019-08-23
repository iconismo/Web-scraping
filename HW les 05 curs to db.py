from zeep import Client
from datetime import datetime as dt
from pprint import pprint
from pymongo import MongoClient

url = 'https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL'

client = Client(url)

month = f'0{6}'
day_from = 1
day_to = 23


# Я подумал, что быстрейший способ найти наиболшую разницу между курсами - это 
# взять разницу между первым и последним элементом в сортированном по значениям словаре

def curs_dict(day_from=day_from, day_to=day_to, month=month):
# ф-ция для формирования словаря (дата: курс валюты). Возвращает словарь.

    curs = {}

    for day in range(day_from, day_to):
        if day < 10:
            day = f'0{day}' # если день месяца до 10, то подставляем строковый "0" для соответствию формату даты в запросе.
            date = f'2019-{month}-{day}'
            money = client.service.GetCursOnDate(date)
            val = money._value_1._value_1[10]['ValuteCursOnDate']['Vcurs']
            curs.update({date: float(val)})

        else:

            date = f'2019-{month}-{day}'
            money = client.service.GetCursOnDate(date)
            val = money._value_1._value_1[10]['ValuteCursOnDate']['Vcurs']
            curs.update({date: float(val)})

    return curs

def sorted_curs(curs_dict):
# ф-ция для сортировки словаря по значениям (от меньшего курса к большему). 
# Возвращает отсортированный словарь

    curs = curs_dict()

    sorted_curs = sorted(curs.items(), key=lambda item: item[1])

    return sorted_curs


def output(sorted_curs, curs_dict):
# ф-ция вывода. Сравнивает ключи (строковые даты) наименьшего и наибольшего значений курса
# в отсортированном словаре первое и последнее значение соответственно.
# Тут я немного перемудрил и надо было сделать функцию по другому, но переделать возможности уже нет.

    curs_dict = sorted_curs(curs_dict)

    sml_val_dat = dt.strptime(curs_dict[0][0], '%Y-%m-%d').date() # дата меньшего курса (первый элем.)
    gt_val_dat = dt.strptime(curs_dict[-1][0], '%Y-%m-%d').date() # дата большего курса (последний элем)

    sml_val = curs_dict[0][1] # меньший курс (первый элем.)
    gt_val = curs_dict[-1][1] # больший курс (последний элем.)

#   если дата большего курса раньше даты меньшего, то они меняются местами в выводе, прибыль всегда положительна.
    if gt_val_dat < sml_val_dat:
        print(f'Валюту USD выгодно было купить {gt_val_dat}, а продать {sml_val_dat}.'
              f' Прибыль: {round(gt_val - sml_val, 4)}')

    else:
        print(f'Валюту USD выгодно было купить {sml_val_dat}, а продать {gt_val_dat}.'
              f' Прибыль: {round(gt_val - sml_val, 4)}')


output(sorted_curs, curs_dict) # вывод по форме в задании ("Валюту USD выгодно было купить...")

dbclient = MongoClient('mongodb://127.0.0.1:27017')

cursdb = dbclient['cursdb']
cursdb = cursdb.cursdb

curs_dict = curs_dict()

# Добавляем в БД данные по каждому дню через цикл
for k, v in curs_dict.items():
    cursdb.insert_one({'date': k, 'curs': v})

# Про веряем данные на наличие в БД    
for i in cursdb.find({}):
    print(i)

# Вывод:

# Forcing soap:address location to HTTPS
# Forcing soap:address location to HTTPS
# Валюту USD выгодно было купить 2019-06-04, а продать 2019-06-22. Прибыль: 2.4252
# {'_id': ObjectId('5d5eff3f3a61801dc8d4e09b'), 'date': '2019-06-01', 'curs': 65.3834}
# {'_id': ObjectId('5d5eff3f3a61801dc8d4e09c'), 'date': '2019-06-02', 'curs': 65.3834}
# {'_id': ObjectId('5d5eff3f3a61801dc8d4e09d'), 'date': '2019-06-03', 'curs': 65.3834}
# {'_id': ObjectId('5d5eff3f3a61801dc8d4e09e'), 'date': '2019-06-04', 'curs': 65.5547}
# {'_id': ObjectId('5d5eff3f3a61801dc8d4e09f'), 'date': '2019-06-05', 'curs': 65.1614}

# И т.д....
