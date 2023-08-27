import psycopg2
import requests
# from test_data import *


def add_user(id, name, target_sex, target_age_min, target_age_max, target_city):
    conn = psycopg2.connect(database='vkinder_db', user='postgres', password='a2887233')
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO users(id, name, target_sex, target_age_min, target_age_max, target_city)
        VALUES(%s, %s, %s, %s, %s, %s);
        """, (id, name, target_sex, target_age_min, target_age_max, target_city))
        conn.commit()
        conn.close()

# def add_user(**kwargs):
#     info = kwargs
#     with conn.cursor() as cur:
#         cur.execute("""
#         INSERT INTO users(id, name, target_sex, target_age_min, target_age_max, target_city)
#         VALUES(%s, %s, %s, %s, %s, %s);
#         """, (kwargs['id'], kwargs['name'], kwargs['target_sex'], kwargs['target_age_min'], kwargs['target_age_max'],
#               kwargs['target_city']))
#         conn.commit()


def update_user_info():
    pass


# def add_favorite(id, name, surname, profile_link):
#     with conn.cursor() as cur:
#         cur.execute("""
#         INSERT INTO favorites(id, name, surname, profile_link)
#         VALUES(%s, %s, %s, %s);
#         """, (id, name, surname, profile_link))
#         conn.commit()


def add_user_favorite(user_id, favorite_id, is_banned=False):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO user_favorite(user_id, favorite_id, is_banned)
        VALUES(%s, %s, %s);
        """, (user_id, favorite_id, is_banned))
        conn.commit()


def add_user_favorite():
    pass


def send_to_blacklist(user_id, favorite_id):
    add_user_favorite(user_id, favorite_id, is_banned=True)


def add_photos(favorite_id, photo_1, photo_2, photo_3):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO photos(favorite_id, photo_1, photo_2, photo_3)
        VALUES(%s, %s, %s, %s);
        """, (favorite_id, photo_1, photo_2, photo_3))
        conn.commit()


def get_user_info(user_id):
    conn = psycopg2.connect(database='vkinder_db', user='postgres', password='a2887233')
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM users WHERE id = %s;
        """, (user_id, ))
        desc = cur.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cur.fetchall()]
        return data[0]


def get_favorite_info(favorite_id):
    conn = psycopg2.connect(database='vkinder_db', user='postgres', password='a2887233')
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM favorites WHERE id = %s;
        """, (favorite_id, ))
        desc = cur.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cur.fetchall()]
        return data[0]


def get_photos(favorite_id):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * FROM photos WHERE favorite_id = %s;
        """, (favorite_id,))
        desc = cur.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cur.fetchall()]
        return data[0]


def get_favorites_list(user_id):
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
        return data[0]


# if __name__ == '__main__':
#     conn = psycopg2.connect(database='vkinder_db', user='postgres', password='a2887233')

    for user in users:
        add_user(**user)
    for favorite in favorites:
        add_favorite(**favorite)
    favorite_id = favorites[3]['id']
    photos = []
    resp = requests.get('https://mykaleidoscope.ru/uploads/posts/2023-05/1684926931_mykaleidoscope-ru-p-plate-natasha-rostova-25.jpg')
    for _ in range(3):
        photos.append(resp.content)
    add_photos(favorite_id, *photos)
    print(get_user_info('48414363'))
    print(get_favorite_info(favorite_id))
    print(get_photos(favorite_id))
    add_user_favorite(55512122, 55512124)
    print(get_favorites_list(55512122))
#     for user in users:
#         add_user(**user)
#     # for favorite in favorites:
#     #     add_favorite(**favorite)
#     # favorite_id = favorites[3]['id']
#     # photos = []
#     # with open('photo_1.jpg', 'rb') as f:
#     #     photos.append(f)
#     # with open('photo_2.jpg', 'rb') as f:
#     #     photos.append(f)
#     # with open('photo_3.jpg', 'rb') as f:
#     #     photos.append(f)
#     # resp = requests.get('https://mykaleidoscope.ru/uploads/posts/2023-05/1684926931_mykaleidoscope-ru-p-plate-natasha-rostova-25.jpg')
#     # for _ in range(3):
#     #     photos.append(resp.content)
#     # add_photos(favorite_id, *photos)
#     # print(get_user_info('48414363'))
#     # print(get_favorite_info(favorite_id))

#     conn.close()
