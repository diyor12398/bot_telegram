from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/Режим_работы')
b2 = KeyboardButton('/Расположение')
b3 = KeyboardButton('/Меню')
kb=ReplyKeyboardMarkup(resize_keyboard=True).row(b3).add(b1).insert(b2)

