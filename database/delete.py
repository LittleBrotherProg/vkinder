import os
import psycopg2
# from psycopg2 import Error
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('user')
password = os.getenv('password')
db = os.getenv('db')


async def delete_favorites_last_viewed(user_id):
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM favorites_viewed
        WHERE user_id = %s;
        """, (user_id,))
    conn.commit()
    conn.close()
    return


async def delete_favorite_(user_id, favorite_id):
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM user_favorite
        WHERE user_id = %s AND favorite_id = %s;
        """, (user_id, favorite_id))
        conn.commit()
        cur.execute("""
        DELETE FROM photos 
        WHERE  favorite_id = %s;
        """, (favorite_id,))
        conn.commit()
        cur.execute("""
        DELETE FROM favorites 
        WHERE id = %s;
        """, (favorite_id,))
        conn.commit()

    conn.commit()
    conn.close()
    return


async def delete_user_last_viewed(user_id):
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM user_viewed
        WHERE user_id = %s;
        """, (user_id,))
    conn.commit()
    conn.close()
    return
