from aiogram import types, Dispatcher
from create_bot import bot, dp
from keyboards import kb
from da import sq_db
async def com_start(message: types.message):
    try:
        await bot.send_message(message.from_user.id, 'Приятного апппетита', reply_markup= kb)
        await message.delete()
    except:
        await message.reply('Приятного апппетита')
async def geol(message: types.message):
    await bot.send_message(message.from_user.id, 'Аргынбекова 45')
async def regim(message: types.message):
    await bot.send_message(message.from_user.id, 'пн-пт по 09,00-18,00\nсуббота 10,00-15,00')
async def mnu(message: types.message):
    await sq_db.men(message)
def register_client(dp: Dispatcher):
    dp.register_message_handler(com_start, commands=['start'])
    dp.register_message_handler(geol, commands=['Расположение'])
    dp.register_message_handler(regim, commands=['Режим_работы'])
    dp.register_message_handler(mnu, commands=['Меню'])