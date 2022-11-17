from aiogram.dispatcher.filters import Text
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from data import add_team, add_user, add_product, get_admins, add_task

from .handlers import get_attr

from dispatcher import dp


# def kb_for_update() -> InlineKeyboardMarkup:
#     buttons = [
#         [
#             InlineKeyboardButton(text='Имя', callback_data='update_name'),
#             InlineKeyboardButton(text='Фамилия', callback_data='update_lastname'),
#             InlineKeyboardButton(text='Номер отряды', callback_data='update_team_code'),
#         ],
#         [
#             InlineKeyboardButton(text='Подтвердить', callback_query='continue')
#         ],
#     ]
#     return InlineKeyboardMarkup(inline_keybord=buttons)
#
#
# @ah.message_handler(
#     Text(text='обновить данные участника', ignore_case=True),
# )
# async def add_user_(msg: Message, state: FSMContext):
#     await msg.answer('Введите код участника')


@dp.message_handler(Text(startswith='добавить задачу', ignore_case=True), lambda msg: msg.from_user.id in get_admins())
async def add_task_(msg: Message):
    cmd = get_attr(msg.text)
    success = add_task(cmd[0], cmd[1], cmd[2])
    if success:
        await msg.answer('Задача добавлена!')
        return

    await msg.answer('Произошла ошибка, но это не точно')


@dp.message_handler(Text(startswith='добавить товар', ignore_case=True), lambda msg: msg.from_user.id in get_admins())
async def add_product_(msg: Message):
    cmd = get_attr(msg.text)

    _ = add_product(cmd[0], cmd[1])

    await msg.answer('Товар добавлен ^_^')


@dp.message_handler(Text(startswith='добавить пользователя', ignore_case=True), lambda msg: msg.from_user.id in get_admins())
async def add_user_(msg: Message):
    cmd = get_attr(msg.text)

    user_code = add_user(cmd[0], cmd[1], cmd[2], cmd[3])

    await msg.answer(f'Пользователь зарегистрирован ^-^ Вот его код - {user_code}')


@dp.message_handler(Text(startswith='', ignore_case=True), lambda msg: msg.from_user.id in get_admins())
async def add_team_(msg: Message):
    cmd = get_attr(msg.text)
