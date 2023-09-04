import os
import psycopg2
from dotenv import load_dotenv

# В терминале выполнить команду: createdb -U postgres vkinder_db


load_dotenv()

user = os.getenv('user')
password = os.getenv('password')
db = os.getenv('db')


def drop_tables():
    conn = psycopg2.connect(database=db, user=user, password=password)
    with conn.cursor() as cur:
        cur.execute('DROP TABLE photos, user_favorite, user_viewed,  users, favorites, favorites_viewed ;')
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
            user_id INTEGER NOT NULL REFERENCES users(id) PRIMARY KEY,
            viewed_id TEXT
        );
        ''')
        conn.commit()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS favorites_viewed(
            user_id INTEGER NOT NULL REFERENCES users(id) PRIMARY KEY,
            viewed_id TEXT
        );
        ''')
        conn.commit()
    conn.close()


if __name__ == '__main__':
    drop_tables()
    create_tables()
