from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin
from da import sq_db

async def on_startup(_):
    print('bot vishel online')
    sq_db.dat()

client.register_client(dp)
admin.re(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)