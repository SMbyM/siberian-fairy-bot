from aiogram.types import *

from data import *
from dispatcher import dp


@dp.message_handler(commands=['start'])
async def start(msg: Message):
    if not data.user_exists(msg.from_user.id):
        await msg.answer('Упс! А тебя нет у меня в списке, подойди к вожатому, попробуем исправить ;)')
        return


