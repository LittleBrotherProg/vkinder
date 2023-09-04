# import os
from database.add import *
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('user')
password = os.getenv('password')
db = os.getenv('db')


async def send_to_blacklist(user_id, **viewed_data_dict):
    """
    Результирующая функция, добавляет новые строки в таблицы favorite, photos, user_favorite, user_viewed
    :param user_id: int
    :param viewed_data_dict: {'id': int, 'name': str, 'surname': str, 'profile_link': str,
    photos: {photo_1: str, photo_2: str, photo_3: str}}
    """
    await add_record_favorite_table(viewed_data_dict['id'], viewed_data_dict['name'], viewed_data_dict['surname'],
                                    viewed_data_dict['profile_link'])
    await add_record_photos_table(viewed_data_dict['id'], **viewed_data_dict['photos'])
    await add_record_user_favorite_table(user_id, viewed_data_dict['id'], is_banned=True)
    await add_record_viewed_table(user_id, viewed_data_dict['id'])


async def add_favorite(user_id, **viewed_data_dict):
    """
    Результирующая функция, добавляет новые строки в таблицы favorite, photos, user_favorite, user_viewed.
    :param user_id: int
    :param viewed_data_dict: {'id': int, 'name': str, 'surname': str, 'profile_link': str,
    photos: {photo_1: str, photo_2: str, photo_3: str}}
    """
    await add_record_favorite_table(viewed_data_dict['id'],
                                    viewed_data_dict['name'],
                                    viewed_data_dict['surname'],
                                    viewed_data_dict['profile_link']
                                    )
    await add_record_photos_table(
        viewed_data_dict['id'],
        **viewed_data_dict['photos']
    )
    await add_record_user_favorite_table(
        user_id,
        viewed_data_dict['id']
    )
    await add_record_viewed_table(
        user_id,
        viewed_data_dict['id']
    )
