import asyncio
from aiogram import Bot, Dispatcher

from app.heandlers import router


async def main():
    bot = Bot(token='6034305301:AAFCiWFQoMQIIee5x2kT62zQJsSXFtyRKSk')
    dp = Dispatcher()
    dp.include_router(router)

    while True:
        await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')

