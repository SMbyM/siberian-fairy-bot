from aiogram import Bot
from aiogram.types import *
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN


bot = Bot(token='5757913178:AAFenicSGytVqJ5zzY1n3GAXs7Y0tKlMZ1o')
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp )

