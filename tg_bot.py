import telebot
import asyncio
from aiogram import Bot, Dispatcher

from app.heandlers import router
from scrapper import scrapping_drom, compare
from url_settings import get_url
import app.keyboards as kb


async def main():
    url = 'https://auto.drom.ru/region54/all/?minprice=500000&minyear=2014&inomarka=1&keywords=срочно'
    bot = Bot(token='6034305301:AAFCiWFQoMQIIee5x2kT62zQJsSXFtyRKSk')
    dp = Dispatcher()
    dp.include_router(router)

    asyncio.create_task(dp.start_polling(bot))

    last_suitable_options = []
    while True:
        url = await get_url()
        suitable_options = await scrapping_drom(url)
        new_car = await compare(suitable_options, last_suitable_options)
        if new_car:
            for car in new_car:
                await bot.send_message(674796107, f'По заданным фильтрам есть новое объявление: \n '
                                                f'Наименование: {car.get("name")}; \n Цена: {car.get("price")}; \n '
                                                f'Ссылка: {car.get("link")} ')
        last_suitable_options = suitable_options
        await asyncio.sleep(300)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')

