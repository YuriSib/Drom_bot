from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb

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
    await message.answer('Выберите радиус поиска', reply_markup=kb.search_radius)


@router.callback_query(lambda callback_query: callback_query.data.startswith('radius_'))
async def cb_choice_radius(callback: CallbackQuery, bot):
    property_radius = callback.data
    user_id = callback.from_user.id

    search_filter['user_id'] = user_id
    search_filter['radius'] = property_radius

    print(f'Пользователь выбрал опцию: {property_radius}')
    await callback.answer('Вы выбрали радиус поиска', show_alert=False)
    await callback.message.answer(f'Вы выбрали {property_radius}')
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await bot.send_message(chat_id=callback.from_user.id, text="Выберите ценовой диапазон:",
                           reply_markup=kb.price_range)


@router.callback_query(lambda callback_query: callback_query.data.startswith('price_'))
async def cb_choice_price(callback: CallbackQuery, bot):
    property_price = callback.data

    search_filter['price'] = property_price

    print(f'Пользователь выбрал опцию: {property_price}')
    await callback.answer('Вы выбрали ценовой диапазон', show_alert=False)
    await callback.message.answer(f'Вы выбрали {property_price}')
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await bot.send_message(chat_id=callback.from_user.id, text="Выберите год выпуска:",
                           reply_markup=kb.year_range)


@router.callback_query(lambda callback_query: callback_query.data.startswith('year_'))
async def cb_choice_year(callback: CallbackQuery, bot):
    property_year = callback.data

    search_filter['year'] = property_year

    print(f'Пользователь выбрал опцию: {property_year}')
    await callback.answer('Вы выбрали год выпуска', show_alert=False)
    await callback.message.answer(f'Вы выбрали {property_year}')
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await bot.send_message(chat_id=callback.from_user.id, text="Выберите страну-производителя:",
                           reply_markup=kb.manufacturer)


@router.callback_query(lambda callback_query: callback_query.data.startswith('from_'))
async def cb_choice_manufacturer(callback: CallbackQuery, bot):
    property_manufacturer = callback.data

    search_filter['manufacturer'] = property_manufacturer

    print(f'Пользователь выбрал опцию: {property_manufacturer}')
    await callback.answer('Вы выбрали год выпуска', show_alert=False)
    await callback.message.answer(f'Бот начнет мониторинг площадки с применением фильтров: \n'
                                  f'Радиус поиска : {search_filter.get("radius")};\n'
                                  f'Ценовой диапазон : {search_filter.get("price")};\n'
                                  f'Годы производства : {search_filter.get("year")};\n'
                                  f'Сделано в : {search_filter.get("manufacturer")}.\n'
                                  f'Нажмите "Продолжить", чтобы начать мониторинг '
                                  f'или "Назад", чтобы задать фильтры с начала.')
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await bot.send_message(chat_id=callback.from_user.id, text='Подтвердите выбор', reply_markup=kb.confirmation)


@router.callback_query(lambda callback_query: callback_query.data.startswith('confirmation_'))
async def cb_choice_confirm(callback: CallbackQuery, bot):
    await callback.answer('Здесь будет набор посказок по теме 2', show_alert=True)
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)


@router.callback_query(lambda callback_query: callback_query.data.startswith('topic_1'))
async def cb_choice_topic1(callback: CallbackQuery, bot):
    await callback.answer('Здесь будет набор посказок по теме 2', show_alert=True)
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)


@router.callback_query(lambda callback_query: callback_query.data.startswith('topic_2'))
async def cb_choice_topic2(callback: CallbackQuery, bot):
    await callback.answer('Здесь будет набор посказок по теме 2', show_alert=True)
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)


# @router.message(lambda callback_query: True)
# async def catalog(message: Message):
#     await message.answer('Выберите радиус поиска', reply_markup=kb.price_range)


@router.message(F.text == '/my_id')
async def cmd_start(message: Message):
    await message.answer(f'Ваш ID: {message.from_user.id}')
    await message.reply(f'Ваше имя: {message.from_user.first_name}')
    # await message.answer_photo(
    #     photo='https://avatars.mds.yandex.net/i?id=45402a31d70daeba1d09d22a36202abdea111f78-8977890-images-thumbs&n=13',
    #     caption='Эта крутая тачка может стать твоей!'
    # )


@router.message(F.text == '/send_image')
async def cmd_send_image(message: Message):
    await message.answer_photo(
        photo='https://www.cischool.ru/wp-content/uploads/2021/03/Depositphotos_105514290_l-2015.jpg',
        caption='Пример отправки фото по URL',
    )
    await message.answer_photo(
        photo='AgACAgIAAxkBAAIDsmUFZ5Oa1PeejPxpZdGhNAK3xVSeAAIPzzEb0rwoSBxFmZvTlWA3AQADAgADeQADMAQ',
        caption='Пример отправки фото по ID'
    )


@router.message(F.document)
async def cmd_dc_id(message: Message):
    await message.answer(message.document.file_id)


@router.message(F.text == '/send_doc')
async def cmd_send_doc(message: Message, bot):
    await message.answer("Документ принят")
    await bot.send_message(chat_id='674796107', text='Вам отправлен документ!')


@router.message(F.document)
async def cmd_get_doc_id(message: Message):
    await message.answer(message.document.file_id)


@router.message(F.photo)
async def cmd_send_photo_id(message: Message):
    await message.answer(message.photo[-1].file_id)


@router.message()
async def echo(message: Message):
    await message.answer('Введенный текст не является командой...')