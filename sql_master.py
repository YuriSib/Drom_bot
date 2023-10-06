import sqlite3 as sq


def create_db():
    with sq.connect('bot.db') as con:
        cur = con.cursor()

        cur.execute("""DROP TABLE IF EXISTS users""")
        cur.execute("""DROP TABLE IF EXISTS ads""")

        cur.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER UNIQUE NOT NULL,
        city TEXT NOT NULL ,
        radius TEXT,
        price TEXT,
        year TEXT
        )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS ads (
        tg_id INTEGER,
        car_id INTEGER UNIQUE NOT NULL,
        link TEXT NOT NULL,
        price TEXT
        )""")


def load_from_sql():
    with sq.connect('bot.db') as con:
        cur = con.cursor()
        sql_query = """
            SELECT user_id, tg_id, city, radius, price, year FROM users
        """
        cur.execute(sql_query)

        result = cur.fetchall()

        return result


def load_id_from_sql(tg_id):
    with sq.connect('bot.db') as con:
        cur = con.cursor()
        sql_query = f"""
            SELECT tg_id, city, radius, price, year FROM users WHERE tg_id == {tg_id}
        """
        cur.execute(sql_query)

        result = cur.fetchall()

        return result[0]


def load_options_from_sql(tg_id, car_id):
    with sq.connect('bot.db') as con:
        cur = con.cursor()

        car_id_string = ", ".join([str(item) for item in car_id])
        sql_query = f"""SELECT car_id, link, price FROM ads WHERE tg_id == {tg_id} AND car_id NOT IN ({car_id_string})"""
        cur.execute(sql_query)

        result = cur.fetchall()

        return result


def save_requirements_in_sql(tg_id, city, radius, price, year):
    with sq.connect('bot.db') as con:
        cur = con.cursor()
        sql_query = f"""
            INSERT OR REPLACE INTO users (tg_id, city, radius, price, year)
            VALUES({tg_id}, '{city}', '{radius}', '{price}', '{year}')
        """
        cur.execute(sql_query)
        con.commit()


def save_options_in_sql(tg_id, car_id, link, price):
    with sq.connect('bot.db') as con:
        cur = con.cursor()
        sql_query = f"""
            INSERT OR REPLACE INTO ads (tg_id, car_id, link, price)
            VALUES({tg_id}, '{car_id}', '{link}', '{price}')
        """
        cur.execute(sql_query)
        con.commit()


def clear_options_in_sql(user_id):
    with sq.connect('bot.db') as con:
        cur = con.cursor()
        sql_query = f"""
            DELETE FROM ads WHERE user_id == {user_id}
        """
        cur.execute(sql_query)
        con.commit()