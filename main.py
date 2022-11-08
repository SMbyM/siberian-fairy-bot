from dispatcher import dp
from aiogram.utils import executor

from config import TOKEN
from handlers import *


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

