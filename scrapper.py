import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth


def settings():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    # options.add_argument("--headless")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    return driver


async def scrapping_drom(url_):
    ua = UserAgent()
    user_agent = ua.random

    headers = {'User-Agent': user_agent}

    response = requests.get(url_, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    options = soup.find_all('a', {'data-ftid': 'bulls-list_bull'})

    suitable_options = []
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

        # if 'хорошая' in estimation or 'отличная' in estimation:
        car = dict([('id', id_), ('estimation', estimation), ('link', lnk), ('price', price)])
        suitable_options.append(car)

    return suitable_options


async def scrapping_avito(url):
    driver = settings()
    driver.get(url=url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    options = soup.find_all('div', {'data-marker': 'item'})

    suitable_options = []
    for option in options:
        item_id = option.get('data-item-id')

        html_link = option.find('a', {'class': 'iva-item-sliderLink-uLz1v'})
        link = html_link.get('href')

        price = option.find('div', {'class': 'iva-item-priceStep-uq2CQ'}).get_text(strip=True)

        car = dict([('id', item_id), ('link', link), ('price', price)])
        suitable_options.append(car)

    return suitable_options


async def search_options(current_list, last_list):
    last_id_list = []
    for last_option in last_list:
        last_id_list.append(last_option.get('id'))

    current_id_list = []
    for suitable_option in current_list:
        current_id_list.append(suitable_option.get('id'))

    list_idx = []
    for current_id in current_id_list:
        if current_id not in last_id_list:
            list_idx.append(current_id_list.index(current_id))

    new_options = []
    for idx in list_idx:
        new_options.append(current_list[idx])

    return new_options


async def compare(suitable_options, last_suitable_options):
    if last_suitable_options:
        new_options = await search_options(suitable_options, last_suitable_options)
    else:
        new_options = await search_options(suitable_options, [])

    return new_options
