import asyncio
from aiogram import Bot, Dispatcher
import os

from app.heandlers import router, send_massage
from sql_master import load_from_sql


# async def loop(id_user_list, bot):
#     while True:
#         for user_id in id_user_list:
#             url = users_dict[user_id]
#             await send_massage(f'last_options_{user_id}.pkl', url, bot, user_id)
#             # await bot.send_message(chat_id=user_id, text='Проверка')
#         await asyncio.sleep(120)


async def main():
    bot = Bot(token='6034305301:AAFCiWFQoMQIIee5x2kT62zQJsSXFtyRKSk')
    dp = Dispatcher()
    dp.include_router(router)

    # id_user_list = await get_user_list()

    await asyncio.gather(dp.start_polling(bot))


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')

