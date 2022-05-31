from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from da import sq_db
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


b1 = KeyboardButton('/Загрузить')
b2 = KeyboardButton('/Удалить')
b4 = KeyboardButton('/Удалить')
kb = ReplyKeyboardMarkup(resize_keyboard=True).add(b1, b2)
b3 = KeyboardButton('Отмена')
kb2 = ReplyKeyboardMarkup(resize_keyboard=True).add(b3)
ID = None

class Adm(StatesGroup):
    ph = State()
    name = State()
    desk = State()
    prc = State()

async def cng(message: types.message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Слушаю вас', reply_markup=kb)
    await message.delete()

async def cm_strt(message: types.message):
    if message.from_user.id == ID:
        await Adm.ph.set()
        await message.reply('Загрузи фото', reply_markup=kb2)

async def cans(message: types.message, state: FSMContext):
    if message.from_user.id == ID:
        crst = await state.get_state()
        if crst is None:
            return
        await state.finish()
        await message.reply('OK')

async def load_ph(message: types.message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await Adm.next()
        await message.reply('Теперь введи название')


async def load_name(message: types.message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await Adm.next()
        await message.reply('Введи описание')

async def load_desk(message: types.message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['desk'] = message.text
        await Adm.next()
        await message.reply('Введи цену')

async def load_prc(message: types.message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['prc'] = message.text
        await sq_db.sq_ad(state)
        await message.reply('Готово', reply_markup=kb)
        await state.finish()

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def dele(callback_query: types.CallbackQuery):
    await sq_db.del_com(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена', show_alert=True)

#@dp.message_handler(commands=['Удалить'])
async def delete_item(message: types.message):
    if message.from_user.id == ID:
        read = await sq_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[-1]}')
            await bot.send_message(message.from_user.id, text='Сверху', reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))


def re(dp: Dispatcher):
    dp.register_message_handler(cm_strt, commands='Загрузить', state=None)
    dp.register_message_handler(delete_item, commands=['Удалить'], state=None)
    dp.register_message_handler(cans, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(cng, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(load_ph, content_types=['photo'], state=Adm.ph)
    dp.register_message_handler(load_name, state=Adm.name)
    dp.register_message_handler(load_desk, state=Adm.desk)
    dp.register_message_handler(load_prc, state=Adm.prc)
    dp.register_message_handler(cans, state="*", commands=['Отмена'])
