import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('user')
password = os.getenv('password')
db = os.getenv('db')


async def update_viewed(user_id, viewed):
    conn = psycopg2.connect(
        database=db,
        user=user,
        password=password
    )
    with conn.cursor() as cur:
        cur.execute(
            """UPDATE user_viewed SET viewed_id = %s WHERE user_id = %s""",
            (viewed, user_id)
        )
        conn.commit()
    conn.close()


async def update_favorite_viewed(user_id, viewed):
    conn = psycopg2.connect(
        database=db,
        user=user,
        password=password
    )
    with conn.cursor() as cur:
        cur.execute(
                    """UPDATE favorites_viewed SET viewed_id = %s WHERE user_id = %s""", 
                    (viewed, user_id)
                    )
        conn.commit()
    conn.close()
