from sqlite3 import connect

db = connect('bot.db')
cur = db.cursor()

print(cur.execute('select * from `users`').fetchall())


def buy(product_id, user_id):
    pass


def user_exists(user_id):
    return bool(len(cur.execute(
        'select * from `users` where id = ?',
        (user_id,)
    ).fetchall()))


def add_product(name, price):
    result = cur.execute('insert into `users`(name, price) values (?, ?)', (name, price,))
    return bool(len(result.fetchall()))


def add_user(user_id, name, lastname, team_number):
    result = cur.execute('insert into `users`(id, name, lastname, team_number, amount) values (?, ?, ?, ?, ?)', (user_id, name, lastname, team_number, 1000,))
    return bool(len(result.fetchall()))
