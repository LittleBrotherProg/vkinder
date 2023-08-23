import psycopg2


# Удалить таблицы.
def drop_tables():
    with conn.cursor() as cur:
        cur.execute('DROP TABLE photos, user_favorite, users, favorites;')
        conn.commit()


# Удалить таблицу.
def drop_table(table_name):
    with conn.cursor() as cur:
        cur.execute(f'DROP TABLE {table_name};')
        conn.commit()


def create_type():
    with conn.cursor() as cur:  # id SERIAL PRIMARY KEY
        cur.execute('''
        CREATE TYPE SEX AS ENUM ('male', 'female', 'both');
                ''')
        conn.commit()


# Функция, создающая структуру БД (таблицы).
def create_tables():
    with conn.cursor() as cur:  # id SERIAL PRIMARY KEY
        cur.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            name VARCHAR(80) NOT NULL,
            target_sex SEX,
            target_age_min INTEGER CHECK (target_age_min >= 18),
            target_age_max INTEGER CHECK (target_age_max >= target_age_min),
            target_city VARCHAR(80)
        );
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS favorites(
            id INTEGER PRIMARY KEY,
            name VARCHAR(80) NOT NULL,
            surname VARCHAR(80),
            profile_link VARCHAR(80) NOT NULL
        );
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS photos(
            favorites_id INTEGER NOT NULL REFERENCES favorites(id),
            photo_1 BYTEA,
            photo_2 BYTEA,
            photo_3 BYTEA
        );
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS user_favorite(
            user_id INTEGER NOT NULL REFERENCES users(id),
            favorite_id INTEGER NOT NULL REFERENCES favorites(id),
            is_banned BOOLEAN DEFAULT FALSE,
            PRIMARY KEY (user_id, favorite_id)
        );
        ''')
        conn.commit()


#
#
# # Функция обработки телефонного номера.
#
# def phone_processing(phone):
#     if len(phone) > 11:
#         return phone[0:-10:], phone[-10:]
#     else:
#         return '+7', phone[-10:]
#
#
# # Получение client_id
#
# def get_client_id(name, surname):
#     with conn.cursor() as cur:
#         cur.execute("""
#         SELECT id FROM clients WHERE name = %s AND surname = %s;
#         """, (name, surname))
#         return cur.fetchall()
#
#
# # Функция, позволяющая добавить нового клиента.
#
# def add_new_client(name, surname, email, phone=None):
#     with conn.cursor() as cur:
#         cur.execute("""
#         INSERT INTO clients(name, surname, email) VALUES(%s, %s, %s);
#         """, (name, surname, email))
#         if phone:
#             client_id = get_client_id(name, surname)[-1]
#             add_phone(client_id, phone)
#         conn.commit()
#
#
# # Функция, позволяющая добавить телефон для существующего клиента.
#
# def add_phone(client_id, phone):
#     with conn.cursor() as cur:
#         ccp = phone_processing(phone)
#         cur.execute("""
#         INSERT INTO phones(client_id, country_code, phone) VALUES(%s, %s, %s);
#         """, (client_id, ccp[0], ccp[1]))
#         conn.commit()
#
#
# # Функция, позволяющая изменить данные о клиенте.
#
# def change_data(client_id, name, surname, email, phone=None):
#     with conn.cursor() as cur:
#         cur.execute("""
#         UPDATE clients SET name = %s, surname = %s, email = %s WHERE id = %s;
#         """, (name, surname, email, client_id))
#         if phone:
#             add_phone(client_id, phone)
#         conn.commit()
#
#
# # Функция, позволяющая удалить телефон для существующего клиента.
#
# def delete_phone(phone):
#     with conn.cursor() as cur:
#         cc_ph = phone_processing(phone)
#         cur.execute("""
#         DELETE FROM phones WHERE country_code = %s AND phone = %s;
#         """, (cc_ph[0], cc_ph[1]))
#         conn.commit()
#
#
# # Функция, позволяющая удалить существующего клиента.
#
#
# def goodbye_client(client_id):
#     with conn.cursor() as cur:
#         cur.execute("""
#         DELETE FROM phones WHERE client_id = %s;
#         DELETE FROM clients WHERE id = %s;
#         """, (client_id, client_id))
#         conn.commit()
#
#
# # Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
#
# def get_client_info(name='%', surname='%', email='%', phone=None):
#     with conn.cursor() as cur:
#         if phone:
#             cc_ph = phone_processing(phone)
#             cur.execute("""
#             SELECT c.id, name, surname, email, country_code, phone FROM clients AS c
#             LEFT JOIN phones AS p ON c.id = p.client_id
#             WHERE country_code = %s AND phone = %s;
#             """, (cc_ph[0], cc_ph[1]))
#         else:
#             cur.execute("""
#             SELECT c.id, name, surname, email, country_code, phone FROM clients AS c
#             LEFT JOIN phones AS p ON c.id = p.client_id
#             WHERE name LIKE %s AND surname LIKE %s AND email LIKE %s;
#             """, (name, surname, email))
#         return cur.fetchall()


if __name__ == '__main__':
    conn = psycopg2.connect(database='vkinder_db', user='postgres', password='314159')
    # drop_tables()
    # drop_table('users')
    create_tables()

    # add_new_client('Иван', 'Иванов', 'iivanov@gmail.com')
    # add_new_client('Петр', 'Иванов', 'PiVanOff@gmail.com', '89101112233')
    # add_new_client('Сергей', 'Иванов', 'sivanov@gmail.com', '+909101112233')
    # add_new_client('Иван', 'Иванов', 'ivivanov@gmail.com')
    # add_phone(4, '89201112233')
    # change_data(2, 'Петр', 'Иванов', 'petrivanov@gmail.com', '89105556677')
    # delete_phone('+79101112233')
    # print(get_client_info('Сергей', 'Иванов', 'sivanov@gmail.com', '+909101112233'))
    # print(get_client_info('Иван'))
    # print(get_client_info(phone='+79105556677'))
    # goodbye_client(2)
    # print(get_client_info())

    conn.close()
