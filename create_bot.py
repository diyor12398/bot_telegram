from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from flask import Flask, request
import os
TOKEN = '5482680028:AAGoSoHtL8dtSo-J2MCWMDFSJTQQfPyPMDk'
URL = f'https://telegram---bot1.herokuapp.com/{TOKEN}'
strg = MemoryStorage()
bot = Bot(token=TOKEN)
server = Flask(__name__)
dp = Dispatcher(bot, storage=strg)

@server.route('/'+TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = types.Update.de_json(json_string)
    bot.process_new_updates(update)
    return '!', 200




@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=URL)
    return '!', 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
