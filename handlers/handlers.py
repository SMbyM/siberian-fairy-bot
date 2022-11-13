from aiogram.types import *
from aiogram.filters import Text

from data import login_user, add_user, get_amount
from dispatcher import dp


def get_attr(str: str) -> list:
    return str.split()[1:]


@dp.message_handler(commands=['start'])
async def start(msg: Message):
    # if not user_exists(msg.from_user.id):
    #     await msg.answer('Упс! А тебя нет у меня в списке, подойди к вожатому, попробуем исправить ;)')
    #     return
    if not add_user(msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name, 0):
        pass
    await msg.answer('Теперь ты в наших рядах!!')


@dp.message_handler(Text(text='счет', ignore_case=True))
async def amount(msg: Message):
    await msg.answer(get_amount(msg.from_user.id))


@dp.message_handler(Text(text='войти', ignore_case=True))
async def log(msg: Message):
    code = get_attr(msg.text)[0]
    info = login_user(msg.from_user.id, code)

    await msg.answer(f'Ура!!! Ты наконец-то с нами, {info[0]}!')


@dp.message_handler(commands=['id'])
async def id(msg: Message):
    await msg.answer(msg.from_user.id)


