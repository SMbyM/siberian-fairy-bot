from sqlite3 import connect

import typing

db = connect('./data/bot.db')
cur = db.cursor()


def execute_query(query: str, values: tuple, mode: str = 'bool') -> typing.Union[bool | list]:
    result = cur.execute(query, values)

    bool_or_list = True if mode == 'bool' else False

    if bool_or_list:
        db.commit()

    return bool(len(result.fetchall())) if bool_or_list else result.fetchall()


def get_amount(user_id: int) -> int:
    return execute_query(
        'select amount from `users` where user_id = ?',
        (user_id,),
        'list'
    )[0][0]


def get_admins() -> list:
    return execute_query(
        'select user_id from `users` where role = \'admin\''
        (),
        'list'
    )


def pay(user_id: int, price: int) -> str:
    amount = get_amount()

    success = False

    if amount < price:
        success = execute_query(
            'update `users` set amount = (? - ?) where user_id = ?',
            (amount, price, user_id,)
        )

    return 'Успешненько!!!' if success is True else 'А у тебя баллов не хватает... -_-'


def buy(product_id: int, user_id: int) -> str:
    return pay(user_id,
                     execute_query(
                         'select price from products where id = ?',
                         (product_id,)
                     )[0])


def login_user(user_id: int, user_code: int) -> list:
    if user_exists(user_id) and is_correct_user_code(user_code):
        return execute_query(
            'select name, lastname, team_code, amount from `users` where user_id = ?',
            (user_id,),
            'list'
        )

    return [False]


def user_exists(user_id: int) -> bool:
    return execute_query(
        'select id from `users` where id = ?',
        (user_id,)
    )


def is_correct_user_code(user_code: int) -> bool:
    return execute_query(
        'select user_id from `users` where user_code = ?',
        (user_code,)
    )


def add_product(name: str, price: int) -> bool:
    return execute_query(
        'insert into `products`(name, price) values (?, ?)',
        (name, price,)
    )


def add_user(user_id: int, name: str, lastname: str, team_number: int, role: str) -> bool:
    return execute_query(
        'insert into `users`(user_id, name, lastname, team_code, amount, role) values (?, ?, ?, ?, ?)',
        (user_id, name, lastname, team_number, 1000, role)
    )


def add_team(leader: str) -> bool:
    return execute_query(
        'insert into `teams`(lead) values (?)',
        (leader,)
    )


