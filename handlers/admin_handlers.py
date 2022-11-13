from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from data import add_team, add_user, add_product, get_admins
from filters import IsAdminFilter

ah = Router()


def kb_for_update() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text='Имя', callback_data='update_name'),
            InlineKeyboardButton(text='Фамилия', callback_data='update_lastname'),
            InlineKeyboardButton(text='Номер отряды', callback_data='update_team_code'),
        ],
        [
            InlineKeyboardButton(text='Подтвердить', callback_query='continue')
        ],
    ]
    return InlineKeyboardMarkup(inline_keybord=buttons)


@ah.message(
    IsAdminFilter(user_id=get_admins()),
    Text(text='обновить данные участника', ignore_case=True),
)
async def add_user_(msg: Message, state: FSMContext):
    await msg.answer('Введите код участника')