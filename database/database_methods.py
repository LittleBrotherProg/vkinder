import os
import psycopg2
from dotenv import load_dotenv
# from test_data import *

load_dotenv()

user = os.getenv('user')
password = os.getenv('password')
db = os.getenv('db')


async def add_user(id, name, target_sex, target_age_min, target_age_max, target_city):
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO  users(id, name, target_sex, target_age_min, target_age_max, target_city)
        VALUES(%s, %s, %s, %s, %s, %s);
        """, (id, name, target_sex, target_age_min, target_age_max, target_city))
        conn.commit()
    conn.close()


def update_user_info():
    pass


async def add_favorite(id, name, surname, profile_link):
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO favorites(id, name, surname, profile_link)
        VALUES(%s, %s, %s, %s);
        """, (id, name, surname, profile_link))
        conn.commit()
    conn.close()


async def add_user_favorite(user_id, favorite_id, is_banned=False):
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO user_favorite(user_id, favorite_id, is_banned)
        VALUES(%s, %s, %s);
        """, (user_id, favorite_id, is_banned))
        conn.commit()
    conn.close()


async def send_to_blacklist(user_id, favorite_id, is_banned=True):
    add_user_favorite(user_id, favorite_id, is_banned)


async def add_photos(favorite_id, photo_1, photo_2, photo_3):
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO photos(favorite_id, photo_1, photo_2, photo_3)
        VALUES(%s, %s, %s, %s);
        """, (favorite_id, photo_1, photo_2, photo_3))
        conn.commit()
    conn.close()


# def add_test_data():
#     for user in users:
#         add_user(**user)
#     for favorite in favorites:
#         add_favorite(**favorite)
#     add_photos(**photos)
#     add_user_favorite(**user_favorite)
#     send_to_blacklist(**blacklist)


async def get_user_info(user_id):
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM users WHERE id = %s;
        """, (user_id, ))
        desc = cur.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cur.fetchall()]
    conn.close()
    if len(data) == 0:
        return data
    return data[0]


async def get_favorite_info(favorite_id):
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


async def get_photos(favorite_id):
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


async def get_favorites_list(user_id):
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


# if __name__ == '__main__':
#     add_test_data()
#     print(get_user_info('48414363'))
#     print(get_favorite_info(55512124))
#     print(get_photos(55512124))
#     print(get_favorites_list(55512122))
#     print(get_user_info('48414363'))
#     print(get_favorite_info('55512124'))
