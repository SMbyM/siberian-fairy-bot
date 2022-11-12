from aiogram.types import *

from data import *
from dispatcher import dp


@dp.message_handler(commands=['start'])
async def start(msg: Message):
    # if not user_exists(msg.from_user.id):
    #     await msg.answer('Упс! А тебя нет у меня в списке, подойди к вожатому, попробуем исправить ;)')
    #     return
    if not add_user(msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name, 0):
        pass
    await msg.answer('Теперь ты в наших рядах!!')


@dp.message_handler(commands=['счет'])
async def amount(msg: Message):
    await msg.answer(get_amount(msg.from_user.id))


@dp.message_handler(commands=['id'])
async def id(msg: Message):
    await msg.answer(msg.from_user.id)


