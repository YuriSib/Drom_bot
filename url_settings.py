
async def get_url(city_, radius_, price_, year_, manufacturer_):
    keywords = f'&keywords=срочно'

    city_dict = {
        'city_msk': 'moscow.',
        'city_spb': 'spb.',
        'city_ekb': 'ekaterinburg.',
        'city_nino': 'nizhniy-novgorod.',
        'city_kras': 'krasnoyarsk.',
        'city_chlb': 'chelyabinsk.',
        'city_smr': 'samara.',
        'city_ufa': 'ufa.',
        'city_rnd': 'rostov-na-donu.',
        'city_krsnd': 'krasnodar.',
        'city_omsk': 'omsk.',
        'city_vrn': 'voronezh.',
        'city_prm': 'perm.',
        'city_vlg': 'volgograd.',
        'city_blg': 'belgorod.',
        'city_sosk': 'stariy-oskol.',
    }
    city = city_dict.get(city_, '')

    radius_dict = {
        '0': '',
        'radius_100': 'distance=100',
        'radius_200': 'distance=200',
        'radius_500': 'distance=500',
        'radius_1000': 'distance=1000'
    }
    radius = radius_dict.get(radius_, '')

    price_dict = {
        'price_100': '&maxprice=100000',
        'price_100-150': '&minprice=100000&maxprice=150000',
        'price_150-200': '&minprice=150000&maxprice=200000',
        'price_200-300': '&minprice=200000&maxprice=300000',
        'price_300-500': '&minprice=300000&maxprice=500000',
        'price_500-800': '&minprice=500000&maxprice=800000',
        'price_800-1200': '&minprice=800000&maxprice=1200000',
        'price_1200-1500': '&minprice=1200000&maxprice=1500000',
        'price_1500': '&minprice=1500000',
    }
    price = price_dict.get(price_, '')

    year_dict = {
        'year_2000-2005': '&minyear=2000&maxyear=2005',
        'year_2000-2010': '&minyear=2000&maxyear=2010',
        'year_2005-2010': '&minyear=2005&maxyear=2010',
        'year_2005-2015': '&minyear=2005&maxyear=2015',
        'year_2010-2015': '&minyear=2010&maxyear=2015',
        'year_2010-2020': '&minyear=2010&maxyear=2020',
        'year_2015-2020': '&minyear=2015&maxyear=2020',
        'year_2015': '&minyear=2015',
        'year_2020': '&minyear=2020',
    }
    year = year_dict.get(year_, '')

    manufacturer_dict = {
        'from_all': '',
        'from_foreign': '?inomarka=1'
    }
    manufacturer = manufacturer_dict.get(manufacturer_, '')

    url = f'https://{city}drom.ru/auto/all/?{radius}{price}{year}{manufacturer}{keywords}'

    return url

