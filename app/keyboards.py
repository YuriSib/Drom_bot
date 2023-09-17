from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardMarkup, InlineKeyboardButton)


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Настроить фильтр'),
     KeyboardButton(text='Справка')],
],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт ниже')


reference = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Тема подсказки 1', callback_data='topic_1')],
    [InlineKeyboardButton(text='Тема подсказки 2', callback_data='topic_2')]
])


search_radius = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='0', callback_data='0')],
    [InlineKeyboardButton(text='100 км', callback_data='radius_100')],
    [InlineKeyboardButton(text='200 км', callback_data='radius_200')],
    [InlineKeyboardButton(text='500 км', callback_data='radius_500')],
    [InlineKeyboardButton(text='1000 км', callback_data='radius_1000')]
])

price_range = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='до 100 тыс.', callback_data='price_100'),
     InlineKeyboardButton(text='100 - 150 тыс.', callback_data='price_100-150')],
    [InlineKeyboardButton(text='150 - 200 тыс.', callback_data='price_150-200'),
     InlineKeyboardButton(text='200 - 300 тыс.', callback_data='price_200-300')],
    [InlineKeyboardButton(text='300 - 500 тыс.', callback_data='price_300-500'),
     InlineKeyboardButton(text='500 - 800 тыс.', callback_data='price_500-800')],
    [InlineKeyboardButton(text='800 тыс. - 1.2 М.', callback_data='price_800-1200'),
     InlineKeyboardButton(text='от 1.2 - 1.5 М.', callback_data='price_1200-1500')],
    [InlineKeyboardButton(text='от 1.5 М.', callback_data='price_1500')]
])

year_range = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='2000 - 2005', callback_data='year_2000-2005'),
     InlineKeyboardButton(text='2000 - 2010', callback_data='year_2000-2010')],
    [InlineKeyboardButton(text='2005 - 2010', callback_data='year_2005-2010'),
     InlineKeyboardButton(text='2005 - 2015', callback_data='year_2005-2015')],
    [InlineKeyboardButton(text='2010 - 2015', callback_data='year_2010-2015'),
     InlineKeyboardButton(text='2010 - 2020', callback_data='year_2010-2020')],
    [InlineKeyboardButton(text='2015 - 2020', callback_data='year_2015-2020'),
     InlineKeyboardButton(text='от 2015', callback_data='year_2015')],
    [InlineKeyboardButton(text='от 2020', callback_data='year_2020')]
])

manufacturer = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Русские и иномарки', callback_data='from_all'),
     InlineKeyboardButton(text='Иномарки', callback_data='from_foreign')],
])

confirmation = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Продолжить', callback_data='confirmation_yes'),
     InlineKeyboardButton(text='Назад', callback_data='confirmation_no')],
])
