import psycopg2

# В терминале выполнить команду: createdb -U postgres vkinder_db


def drop_tables():
    with conn.cursor() as cur:
        cur.execute('DROP TABLE photos, user_favorite, users, favorites;')
        conn.commit()


def drop_table(table_name):
    with conn.cursor() as cur:
        cur.execute(f'DROP TABLE {table_name};')
        # cur.execute('DROP TABLE %s;', (table_name,))
        conn.commit()


def create_type():
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TYPE SEX AS ENUM ('male', 'female', 'both');
                ''')
        conn.commit()


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


if __name__ == '__main__':
    conn = psycopg2.connect(database='vkinder_db', user='postgres', password='a2887233')
    # drop_tables()
    # drop_table('users')
    create_type()
    create_tables()

    conn.close()
