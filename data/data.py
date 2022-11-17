from sqlite3 import connect

import typing

db = connect('./data/bot.db')
cur = db.cursor()


def execute_query(query: str, values: tuple) -> list:
    result = cur.execute(query, values)

    db.commit()

    return result.fetchall()


def get_amount(user_id: int) -> int:
    return execute_query(
        'select amount from `users` where user_id = ?',
        (user_id,)
    )[0]


def get_admins() -> list:
    return (execute_query(
        'select user_id from `users` where role = \'admin\'',
        ()
    ))[0]


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
               )[0]
               )


def login_user(user_id: int, user_name: str, user_code: int) -> list:
    print(user_exists(user_id))
    if not user_exists(user_id) and is_correct_user_code(user_code):
        _ = execute_query(
            'update `users` set (user_id, user_name) = (?, ?) where user_code = ?',
            (user_id, user_name, user_code,)
        )

        return execute_query(
            'select name from `users` where user_id = ?',
            (user_id,)
        )

    return [False]


def get_tasks() -> list:
    return execute_query(
        'select * from `task_list`',
        ()
    )


def user_exists(user_id: int) -> bool:
    return bool(len(execute_query(
        'select id from `users` where user_id = ?',
        (user_id,)
    )))


def is_correct_user_code(user_code: int) -> bool:
    return bool(len(execute_query(
        'select user_id from `users` where user_code = ?',
        (user_code,)
    )))


def add_product(name: str, price: int) -> bool:
    return execute_query(
        'insert into `products`(name, price) values (?, ?)',
        (name, price,)
    )


def add_user(name: str, lastname: str, team_number: int, role: str) -> bool:
    _ = execute_query(
        'insert into `users`(name, lastname, team_code, amount, role) values (?, ?, ?, ?)',
        (name, lastname, team_number, 1000, role)
    )

    return execute_query(
        'select user_code from `users` where (name, lastname) = (?, ?)',
        (name, lastname)
    )[0][0]


def add_team(leader: str) -> bool:
    return execute_query(
        'insert into `teams`(lead) values (?)',
        (leader,)
    )


def add_task(date: str, name: str, time: str) -> bool:
    _ = execute_query(
        'insert into `task`(name, time_for) values (?, ((TIME(?))))',
        (name, time,)
    )
    task_id = execute_query(
        'select id from `task` where (name, time_for) = (?, ?)',
        (name, time)
    )

    day_id = execute_query(
        'select id from `day` where date_ = ((DATE(?)))',
        (date,)
    )

    return bool(len(
        execute_query(
            'insert into `task_day`(day_id, task_id) values (?, ?)',
            (day_id, task_id)
        )
    ))


def get_user_team(user_id: int) -> int:
    return execute_query(
        'select team_number from `users` where user_id = ?',
        (user_id,)
    )[0][0]


def get_leader_of_user_team(user_id: int) -> list:
    team_id = get_user_team(user_id)

    leaders = execute_query(
        'select leader_id from `leader_team` where team_id = ?',
        (team_id,)
    )

    leader_1 = execute_query(
        'select user_id, name, lastname from `users` where id = ?',
        (leaders[0][0],)
    )[0]

    leader_2 = execute_query(
        'select user_id, name, lastname from `users` where id = ?',
        (leaders[1][0],)
    )[0]

    return [leader_1, leader_2]


def get_user_ref(user_id: int) -> str:
    return f"""https://t.me/{execute_query(
        "select user_name from `users` where user_id = ?",
        ())[0][0]}"""
