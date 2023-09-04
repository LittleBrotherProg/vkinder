import os
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv


load_dotenv()

user = os.getenv('user')
password = os.getenv('password')
db = os.getenv('db')

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
    return data


async def get_favorite_info(**params):
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute("""
        SELECT profile_link, name, surname, p.photo_1, p.photo_2, p.photo_3 
        FROM favorites f
        JOIN photos AS p ON f.id = p.favorite_id
        WHERE id = %s;
        """, (params["owner_id"], ))
        desc = cur.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cur.fetchall()]
    conn.close()
    if len(data) == 0:
        return data
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


async def get_last_viewed(user_id):
    """
    :param user_id: int
    :return: id of last viewed person, int
    """
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute("""
        SELECT viewed_id FROM user_viewed WHERE user_id = %s;
        """, (user_id, ))
        data = cur.fetchall()[0][0]
    conn.close()
    return data

async def get_favorites_viewed_id(user_id):
    """
    :param user_id: int
    :return: id of last viewed person, int
    """
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute("""
        SELECT viewed_id FROM favorites_viewed WHERE user_id = %s;
        """, (user_id, ))
        data = cur.fetchall()
        if len(data) == 0:
            conn.close()
            return []
        data = data[0][0]
    conn.close()
    return data

async def get_all_favorites(user_id):
    """
    :param user_id: int
    :return: list of dicts like this:
    [413413414134, 1241421241 ...]
    """
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute("""
        SELECT favorite_id
        FROM user_favorite uf
        WHERE user_id = %s AND is_banned = FALSE;
        """, (user_id,))
        data = [row[0] for row in cur.fetchall()]
    conn.close()
    return data

async def get_black_list(user_id):
    """
    :param user_id: int
    :return: list of dicts like this:
    [413413414134, 1241421241 ...]
    """
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute("""
        SELECT favorite_id 
        FROM user_favorite 
        WHERE user_id = %s AND is_banned = True;
        """, (user_id, ))
        data = [row[0] for row in cur.fetchall()]
    conn.close()
    return data