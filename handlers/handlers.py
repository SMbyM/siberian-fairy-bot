from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from data import login_user, get_amount, get_tasks, get_leader_of_user_team, get_user_ref
from dispatcher import dp


def get_attr(str):
    return str.split()[1:]


@dp.message_handler(commands=['start'])
async def start(msg: Message):
    cmd = get_attr(msg.text)
    if cmd:
        info = login_user(msg.from_user.id, msg.from_user.username, int(cmd[0]))
        if info[0] is not None and info[0] is not False:
            await msg.answer(f'Ура!! Ты теперь с нами, {info[0][0]}!!')
            return
        await msg.answer('Упс! А тебя я не знаю -_-. Подойди к вожатому, попробуем решить вопрос)')
        return
    await msg.answer('Напиши мне заново, но введи свой код участника (Если что, его можно узнать у вожатого ^-^)')


@dp.message_handler(Text(startswith='счет', ignore_case=True))
async def amount(msg: Message):
    await msg.answer(get_amount(msg.from_user.id)[0])


@dp.message_handler(Text(startswith='задачи на день', ignore_case=True), Text(startswith='задачи', ignore_case=True))
async def task_list(msg: Message):
    task = get_tasks()
    tasklist = ''.join([f'{x[0]} - {x[1]}\n' for x in task])

    await msg.answer(tasklist)


@dp.message_handler(Text(startswith='написать вожатому', ignore_case=True))
async def msg_for_leader(msg: Message, state: FSMContext):
    leaders = get_leader_of_user_team(msg.from_user.id)

    await state.set_data({1: leaders[0], 2: leaders[1]})

    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=f'{leaders[0][0]} {leaders[0][1]}', callback_data='leader_1'),
                InlineKeyboardButton(text=f'{leaders[1][0]} {leaders[1][1]}', callback_data='leader_2')
            ],
        ]
    )

    await msg.answer(f'Какому важатому ты хочешь написать?', reply_markup=kb)


@dp.callback_query_handler(Text(startswith='leader_'))
async def query_handler(callback: CallbackQuery, state: FSMContext):
    leader = await state.get_data(int(callback.data.split('_')[1]))
    ref = get_user_ref(leader[0])

    await callback.message.answer(f'Напиши вожатому напрямую, вот ссылка {ref} ^_^')


@dp.message_handler()
async def pay_user(msg: Message):
    pass
# @dp.message_handler(commands=['id'])
# async def id(msg: Message):
#     await msg.answer(msg.from_user.id)


