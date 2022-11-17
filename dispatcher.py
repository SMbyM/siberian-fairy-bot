from aiogram import Bot
from aiogram import Dispatcher

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
