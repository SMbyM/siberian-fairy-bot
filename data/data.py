from aiosqlite import connect

import typing

db = connect('./data/bot.db')
cur = db.cursor()


async def execute_query(query: str, values: tuple, mode: str = 'bool') -> typing.Union[bool | list]:
    result = await cur.execute(query, values)

    bool_or_list = True if mode == 'bool' else False

    if bool_or_list:
        await db.commit()

    return bool(len(result.fetchall())) if bool_or_list else await result.fetchall()


async def get_amount(user_id: int) -> int:
    return await execute_query(
        'select amount from `users` where user_id = ?',
        (user_id,),
        'list'
    )[0]


async def pay(user_id: int, price: int) -> str:
    amount = await get_amount()

    success = False

    if amount < price:
        success = await execute_query(
            'update `users` set amount = (? - ?) where user_id = ?',
            (amount, price, user_id,)
        )

    return 'Успешненько!!!' if success is True else 'А у тебя баллов не хватает... -_-'


async def buy(product_id: int, user_id: int) -> str:
    return await pay(user_id,
                     await execute_query(
                         'select price from products where id = ?',
                         (product_id,)
                     )[0])


async def login_user(user_id: int, user_code: int) -> list:
    if await user_exists(user_id) and await is_correct_user_code(user_code):
        return await execute_query(
            'select name, lastname, team_code, amount from `users` where user_id = ?',
            (user_id,),
            'list'
        )

    return [False]


async def user_exists(user_id: int) -> bool:
    return await execute_query(
        'select id from `users` where id = ?',
        (user_id,)
    )


async def is_correct_user_code(user_code: int) -> bool:
    return await execute_query(
        'select user_id from `users` where user_code = ?',
        (user_code,)
    )


async def add_product(name: str, price: int) -> bool:
    return await execute_query(
        'insert into `products`(name, price) values (?, ?)',
        (name, price,)
    )


async def add_user(user_id: int, name: str, lastname: str, team_number: int, role: str) -> bool:
    return await execute_query(
        'insert into `users`(user_id, name, lastname, team_code, amount, role) values (?, ?, ?, ?, ?)',
        (user_id, name, lastname, team_number, 1000, role)
    )


async def add_team(leader: str) -> bool:
    return await execute_query(
        'insert into `teams`(lead) values (?)',
        (leader,)
    )


