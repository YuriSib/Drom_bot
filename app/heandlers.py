import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb
import os

from scrapper import scrapping_drom, compare
from url_settings import get_url
from work_to_file import load_from_pickle, save_to_pickle

router = Router()

search_filter = {}


@router.message(F.text == '/start')
async def cmd_start(message: Message):
    await message.answer('Миру Мир!', reply_markup=kb.main)


@router.message(F.text == 'Справка')
async def contacts(message: Message):
    await message.answer('Здесь будут посказки, как пользоваться ботом и какой функционал у него есть:',
                         reply_markup=kb.reference)


@router.message(F.text == 'Настроить фильтр')
async def catalog(message: Message):
    await message.answer('Выберите ваш город (если вашего города нет в списке, напишите об этом в поддержку мы добавим '
                         'его течении суток):', reply_markup=kb.searching_city)


@router.callback_query(lambda callback_query: callback_query.data.startswith('city_'))
async def cb_choice_radius(callback: CallbackQuery, bot):
    property_city = callback.data
    user_id = callback.from_user.id

    search_filter['user_id'] = user_id
    search_filter['city'] = property_city

    await callback.answer('Вы выбрали радиус поиска', show_alert=False)
    await callback.message.answer(f'Вы выбрали {property_city}')
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await bot.send_message(chat_id=callback.from_user.id, text="Выберите радиус поиска:",
                           reply_markup=kb.search_radius)


@router.callback_query(lambda callback_query: callback_query.data.startswith('radius_'))
async def cb_choice_price(callback: CallbackQuery, bot):
    property_radius = callback.data
    user_id = callback.from_user.id

    search_filter['radius'] = property_radius

    await callback.answer('Вы выбрали радиус поиска', show_alert=False)
    await callback.message.answer(f'Вы выбрали {property_radius}')
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await bot.send_message(chat_id=callback.from_user.id, text="Выберите ценовой диапазон:",
                           reply_markup=kb.price_range)


@router.callback_query(lambda callback_query: callback_query.data.startswith('price_'))
async def cb_choice_year(callback: CallbackQuery, bot):
    property_price = callback.data

    search_filter['price'] = property_price

    await callback.answer('Вы выбрали ценовой диапазон', show_alert=False)
    await callback.message.answer(f'Вы выбрали {property_price}')
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await bot.send_message(chat_id=callback.from_user.id, text="Выберите год выпуска:",
                           reply_markup=kb.year_range)


@router.callback_query(lambda callback_query: callback_query.data.startswith('year_'))
async def cb_choice_manufacturer(callback: CallbackQuery, bot):
    property_year = callback.data

    search_filter['year'] = property_year

    await callback.answer('Вы выбрали год выпуска', show_alert=False)
    await callback.message.answer(f'Вы выбрали {property_year}')
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await bot.send_message(chat_id=callback.from_user.id, text="Выберите страну-производитель:",
                           reply_markup=kb.manufacturer)


@router.callback_query(lambda callback_query: callback_query.data.startswith('from_'))
async def cb_confirm(callback: CallbackQuery, bot):
    property_manufacturer = callback.data

    search_filter['manufacturer'] = property_manufacturer

    await callback.answer('Вы выбрали год выпуска', show_alert=False)
    await callback.message.answer(f'Бот начнет мониторинг площадки с применением фильтров: \n'
                                  f'Город : {search_filter.get("city")};\n'
                                  f'Радиус поиска : {search_filter.get("radius")};\n'
                                  f'Ценовой диапазон : {search_filter.get("price")};\n'
                                  f'Годы производства : {search_filter.get("year")};\n'
                                  f'Сделано в : {search_filter.get("manufacturer")}.\n'
                                  f'Нажмите "Продолжить", чтобы начать мониторинг '
                                  f'или "Назад", чтобы задать фильтры с начала.')
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await bot.send_message(chat_id=callback.from_user.id, text='Подтвердите выбор', reply_markup=kb.confirmation)


async def send_massage(user_filename, url, bot, user_id):
    last_suitable_options = await load_from_pickle(user_filename) if os.path.isfile(user_filename) else []
    suitable_options = await scrapping_drom(url)
    new_car = await compare(suitable_options, last_suitable_options)
    if new_car:
        for car in new_car:
            await bot.send_message(user_id, f'По заданным фильтрам есть новое объявление: \n '
                                            f'Наименование: {car.get("name")}; \n Цена: {car.get("price")}; \n '
                                            f'Ссылка: {car.get("link")} ')
    await save_to_pickle(user_filename, suitable_options)


@router.callback_query(lambda callback_query: callback_query.data.startswith('confirmation_yes'))
async def cb_start_monitoring(callback: CallbackQuery, bot):
    print(f'Пользователь настроил фильтр слеующим образом: {search_filter}')

    user_id = callback.from_user.id

    await bot.delete_message(chat_id=user_id, message_id=callback.message.message_id)
    await bot.send_message(chat_id=user_id, text='Начинаю мониторинг выдачи по указанным фильтрам')

    city, radius, price, year, manufacturer = search_filter.get("city"), search_filter.get("radius"), \
        search_filter.get("price"), search_filter.get("year"), search_filter.get("manufacturer")

    url = await get_url(city, radius, price, year, manufacturer)

    users_dict = await load_from_pickle('users_dict.pkl') if os.path.isfile('users_dict.pkl') else {}
    users_dict[str(user_id)] = url
    await save_to_pickle('users_dict.pkl', users_dict)

    user_filename = f'last_options_{user_id}.pkl'

    await send_massage(user_filename, url, bot, user_id)


@router.callback_query(lambda callback_query: callback_query.data.startswith('topic_1'))
async def cb_choice_topic1(callback: CallbackQuery, bot):
    await callback.answer('Здесь будет набор подсказок по теме 2', show_alert=True)
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)


@router.callback_query(lambda callback_query: callback_query.data.startswith('topic_2'))
async def cb_choice_topic2(callback: CallbackQuery, bot):
    await callback.answer('Здесь будет набор посказок по теме 2', show_alert=True)
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)


@router.message(F.text == '/my_id')
async def cmd_start(message: Message):
    await message.answer(f'Ваш ID: {message.from_user.id}')
    await message.reply(f'Ваше имя: {message.from_user.first_name}')


@router.message()
async def echo(message: Message):
    await message.answer('Введенный текст не является командой...')