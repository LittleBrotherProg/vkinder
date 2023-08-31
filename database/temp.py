import os
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv


load_dotenv()

user = os.getenv('user')
password = os.getenv('password')
db = os.getenv('db')


# class SukaBlyad:
#
#     load_dotenv()
#
#     def __init__(self):
#         self.conn = psycopg2.connect(database=os.getenv('db'), user=os.getenv('user'), password=os.getenv('password'))
#
#     def close_connection(self):
#         self.conn.close()
#
#     def get_user_info(user_id, self):
#         with self.conn.cursor() as cur:
#             cur.execute("""
#             SELECT * FROM users WHERE id = %s;
#             """, (user_id, ))
#             desc = cur.description
#             column_names = [col[0] for col in desc]
#             data = [dict(zip(column_names, row)) for row in cur.fetchall()]
#             return data[0]


# def connect(func):
#     def new_func(*args, **kwargs):
#         conn = psycopg2.connect(database='vkinder_db', user='postgres', password='314159')
#         result = func(*args, **kwargs)
#         conn.close()
#         return result
#     return new_func


def drop_tables():
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute('DROP TABLE photos, user_favorite, user_viewed, users, favorites;')
        conn.commit()
    conn.close()


# create_tables
def create_tables():
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            name VARCHAR(80) NOT NULL,
            target_sex BOOLEAN DEFAULT NULL,
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
            favorite_id INTEGER NOT NULL REFERENCES favorites(id),
            photo_1 VARCHAR(40),
            photo_2 VARCHAR(40),
            photo_3 VARCHAR(40)
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
        cur.execute('''
        CREATE TABLE IF NOT EXISTS user_viewed(
            user_id INTEGER NOT NULL REFERENCES users(id),
            viewed_id INTEGER NOT NULL,
            PRIMARY KEY (user_id, viewed_id)
        );
        ''')
        conn.commit()
    conn.close()


if __name__ == '__main__':
    drop_tables()
    create_tables()


# test data
users = [
    {'id': 48414363, 'name': 'Иван', 'target_sex': False,
     'target_age_min': 25, 'target_age_max': 32, 'target_city': 'Ярославль'},
    {'id': 55512121, 'name': 'Вера', 'target_sex': True,
     'target_age_min': 25, 'target_age_max': 32, 'target_city': 'Москва'},
    {'id': 55512122, 'name': 'Анатолий', 'target_sex': False,
     'target_age_min': 18, 'target_age_max': 24, 'target_city': 'Санкт-Петербург'},
    {'id': 55512123, 'name': 'Андрей', 'target_sex': False,
     'target_age_min': 16, 'target_age_max': 18, 'target_city': 'Москва'},
    {'id': 55512124, 'name': 'Наталья'},
    {'id': 55512125, 'name': 'Ипполит', 'target_sex': False,
     'target_age_min': 30, 'target_age_max': 35, 'target_city': 'Казань'}
]

favorites = [
    {'id': 55500111, 'name': 'Марья', 'surname': 'Болконская', 'profile_link': 'https://vk.com/id55500111',
     'photos': {'photo_1': 111, 'photo_2': 222, 'photo_3': 333}},
    {'id': 55500112, 'name': 'Елена', 'surname': 'Курагина', 'profile_link': 'https://vk.com/id55500112',
     'photos': {'photo_1': 111}},
    {'id': 55500113, 'name': 'Пётр', 'surname': 'Безухов', 'profile_link': 'https://vk.com/id55500113',
     'photos': {'photo_1': 111, 'photo_2': 222, 'photo_3': 333}},
    {'id': 55512124, 'name': 'Наталья', 'surname': 'Ростова', 'profile_link': 'https://vk.com/id55512124',
     'photos': {'photo_1': 111, 'photo_3': 333}}
]

user_favorite = {'user_id': 55512122, 'favorite_id': 55512124}


def add_record_user_table(id, name, target_sex=None, target_age_min=18, target_age_max=99, target_city=None):
    """
    # Создает запись в таблице users. Обязательно передать параметры id, name.
    :param id: int
    :param name: str
    :param target_sex: bool (True - мужской, False - женский, None - не важно)
    :param target_age_min: int (>=18)
    :param target_age_max: int (>=target_age_min)
    :param target_city: str
    """
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        try:
            cur.execute("""
            INSERT INTO  users(id, name, target_sex, target_age_min, target_age_max, target_city)
            VALUES(%s, %s, %s, %s, %s, %s);
            """, (id, name, target_sex, target_age_min, target_age_max, target_city))
            conn.commit()
        except(Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            conn.close()


def update_user_info(id, name, target_sex=None, target_age_min=18, target_age_max=99, target_city=None):
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute("""UPDATE users SET name = %s WHERE id = %s""", (name, id))
        cur.execute("""UPDATE users SET target_sex = %s WHERE id = %s""", (target_sex, id))
        cur.execute("""UPDATE users SET target_age_min = %s WHERE id = %s""", (target_age_min, id))
        cur.execute("""UPDATE users SET target_age_max = %s WHERE id = %s""", (target_age_max, id))
        cur.execute("""UPDATE users SET target_city = %s WHERE id = %s""", (target_city, id))
        conn.commit()
    conn.close()


def add_record_favorite_table(id, name, surname, profile_link):
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        try:
            cur.execute("""
            INSERT INTO favorites(id, name, surname, profile_link)
            VALUES(%s, %s, %s, %s);
            """, (id, name, surname, profile_link))
            conn.commit()
        except(Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            conn.close()


def add_record_user_favorite_table(user_id, favorite_id, is_banned=False):
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        try:
            cur.execute("""
            INSERT INTO user_favorite(user_id, favorite_id, is_banned)
            VALUES(%s, %s, %s);
            """, (user_id, favorite_id, is_banned))
            conn.commit()
        except(Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            conn.close()


def add_record_photos_table(favorite_id, photo_1=None, photo_2=None, photo_3=None):
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        try:
            cur.execute("""
            INSERT INTO photos(favorite_id, photo_1, photo_2, photo_3)
            VALUES(%s, %s, %s, %s);
            """, (favorite_id, photo_1, photo_2, photo_3))
            conn.commit()
        except(Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            conn.close()


def add_record_viewed_table(user_id, viewed_id):
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        try:
            cur.execute("""
            INSERT INTO user_viewed(user_id, viewed_id)
            VALUES(%s, %s);
            """, (user_id, viewed_id))
            conn.commit()
        except(Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            conn.close()


def add_test_data():
    """
    Заполняет таблицы тестовыми данными
    """
    for user in users:
        add_record_user_table(**user)
    for favorite in favorites:
        add_favorite(55512122, favorite)
    send_to_blacklist(55512121, favorites[-1])
    add_record_viewed_table(55512121, 55512124)
    add_record_viewed_table(55512121, 55500112)
    update_user_info(**{'id': 55512121, 'name': 'Вера', 'target_sex': True,
     'target_age_min': 25, 'target_age_max': 32, 'target_city': 'Санкт-Петербург'})


def get_user_info(user_id):
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM users WHERE id = %s;
        """, (user_id, ))
        desc = cur.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cur.fetchall()]
    conn.close()
    return data[0]


def get_favorite_info(favorite_id):
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM favorites WHERE id = %s;
        """, (favorite_id, ))
        desc = cur.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cur.fetchall()]
    conn.close()
    return data[0]


def get_photos(favorite_id):
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM photos WHERE favorite_id = %s;
        """, (favorite_id,))
        desc = cur.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cur.fetchall()]
    conn.close()
    return data[0]


def get_last_viewed(user_id):
    """
    :param user_id: int
    :return: id of last viewed person, int
    """
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute("""
        SELECT viewed_id FROM user_viewed WHERE user_id = %s;
        """, (user_id, ))
        data = cur.fetchall()[-1][0]
    conn.close()
    return data


# Результирующие функции для кнопок действия

def send_to_blacklist(user_id, viewed_data_dict):
    """
    Результирующая функция, добавляет новые строки в таблицы favorite, photos, user_favorite, user_viewed
    :param user_id: int
    :param viewed_data_dict: {'id': int, 'name': str, 'surname': str, 'profile_link': str,
    photos: {photo_1: str, photo_2: str, photo_3: str}}
    """
    add_record_favorite_table(viewed_data_dict['id'], viewed_data_dict['name'], viewed_data_dict['surname'],
                              viewed_data_dict['profile_link'])
    add_record_photos_table(viewed_data_dict['id'], **viewed_data_dict['photos'])
    add_record_user_favorite_table(user_id, viewed_data_dict['id'], is_banned=True)
    add_record_viewed_table(user_id, viewed_data_dict['id'])


def add_favorite(user_id, viewed_data_dict):
    """
    Результирующая функция, добавляет новые строки в таблицы favorite, photos, user_favorite, user_viewed.
    :param user_id: int
    :param viewed_data_dict: {'id': int, 'name': str, 'surname': str, 'profile_link': str,
    photos: {photo_1: str, photo_2: str, photo_3: str}}
    """
    add_record_favorite_table(viewed_data_dict['id'], viewed_data_dict['name'], viewed_data_dict['surname'],
                              viewed_data_dict['profile_link'])
    add_record_photos_table(viewed_data_dict['id'], **viewed_data_dict['photos'])
    add_record_user_favorite_table(user_id, viewed_data_dict['id'])
    add_record_viewed_table(user_id, viewed_data_dict['id'])


def get_favorites_list(user_id):
    """
    :param user_id: int
    :return: list of dicts like this:
    [{'profile_link': 'https://vk.com/id55512124', 'name': 'Наталья', 'surname': 'Ростова',
    'photo_1': '111', 'photo_2': None, 'photo_3': '333'}, ...]
    """
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute("""
        SELECT f.profile_link, f.name, f.surname, p.photo_1, p.photo_2, p.photo_3
        FROM user_favorite uf
        JOIN favorites AS f ON f.id = uf.favorite_id
        JOIN photos AS p ON f.id = p.favorite_id
        WHERE user_id = %s AND is_banned = FALSE;
        """, (user_id,))
        desc = cur.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cur.fetchall()]
    conn.close()
    return data


if __name__ == '__main__':
    add_test_data()
    print(1, get_user_info('48414363'))
    print(2, get_favorite_info(55512124))
    print(3, get_photos(55512124))
    print(4, get_favorites_list(55512122))
    print(5, get_user_info(55512124))
    print(6, get_favorite_info('55512124'))
    print(7, get_last_viewed(55512122))
