import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from seleniumbase import SB
import pickle
import os

url = 'https://auto.drom.ru/region54/all/?minprice=1500000&minyear=2014&inomarka=1&keywords=срочно'


def scrapping_drom(url_):
    ua = UserAgent()
    user_agent = ua.random

    headers = {'User-Agent': user_agent}

    response = requests.get(url_, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    options = soup.find_all('a', {'data-ftid': 'bulls-list_bull'})

    suitable_options = []
    list_id = []
    for option in options:
        price = option.find('span', {'data-ftid': 'bull_price'}).get_text(strip=True).replace('\xa0', '.')
        lnk = option.get('href')
        id_ = lnk.split('/')[-1].split('.')[0]

        html_name = option.find('div', {'class': 'css-1wgtb37 e3f4v4l2'})
        if html_name:
            name = html_name.get_text(strip=True)

        html_estimation = option.find('div', {'class': 'css-11m58oj evjskuu0'})
        if html_estimation:
            estimation = html_estimation.get_text(strip=True)
        else:
            estimation = 'без оценки'

        if 'хорошая' in estimation or 'отличная' in estimation:
            car = dict([('id', id_), ('estimation', estimation), ('name', name), ('link', lnk), ('price', price)])
            suitable_options.append(car)
            list_id.append(id_)

    return suitable_options, list_id


def compare(suitable_options, list_id):
    if os.path.isfile('list_id.pkl'):
        with open('list_id.pkl', 'rb') as file:
            last_list_id = pickle.load(file)

        new_car_id = [id_ for id_ in list_id if id_ not in last_list_id]

        new_car = None
        for car in suitable_options:
            if car.get('id') in new_car_id:
                new_car = car
                break
    else:
        new_car = suitable_options

    with open('suitable_options.pkl', 'wb') as file:
        pickle.dump(suitable_options, file)
    with open('list_id.pkl', 'wb') as file:
        pickle.dump(list_id, file)

    return new_car
