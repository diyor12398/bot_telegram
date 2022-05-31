import sqlite3 as sq
from create_bot import bot

def dat():
    global base, cur
    base = sq.connect('magz.db')
    cur = base.cursor()
    if base:
        print('ok')

async def sq_ad(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES(?, ?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()

async def del_com(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()

async def men(message):
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo( message.from_user.id, ret[0], f'{ret[1]}\nОписание:  {ret[2]}\nЦена: {ret[-1]}')