import os
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('user')
password = os.getenv('password')
db = os.getenv('db')


async def add_record_favorite_table(id, name, surname, profile_link):
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


async def add_record_user_favorite_table(user_id, favorite_id, is_banned=False):
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


async def add_record_photos_table(favorite_id, photo_1=None, photo_2=None, photo_3=None):
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


async def add_record_viewed_table(user_id, viewed_id):
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


async def add_record_favorite_viewed_table(user_id, viewed_id):
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        try:
            cur.execute("""
            INSERT INTO favorites_viewed(user_id, viewed_id)
            VALUES(%s, %s);
            """, (user_id, viewed_id))
            conn.commit()
        except(Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            conn.close()


async def add_record_user_table(id, name, target_sex=None, target_age_min=18, target_age_max=99, target_city=None):
    """
    Создает запись в таблице users. Обязательно передать параметры id, name.
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
