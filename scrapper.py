import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


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


async def search_options(current_list, last_list):
    last_id_list = []
    for last_option in last_list:
        last_id_list.append(last_option.get('id'))

    current_id_list = []
    for suitable_option in current_list:
        current_id_list.append(suitable_option.get('id'))

    list_idx = []
    for current_id in current_id_list:
        try:
            idx_last_id = last_id_list.index(current_id)
        except ValueError:
            idx_last_id = False
        if idx_last_id is False:
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
