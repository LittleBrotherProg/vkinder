users = [
    {'id': 48414363, 'name': 'Иван', 'target_sex': 'female',
     'target_age_min': 25, 'target_age_max': 32, 'target_city': 'Ярославль'},
    {'id': 55512121, 'name': 'Вера', 'target_sex': 'male',
     'target_age_min': 25, 'target_age_max': 32, 'target_city': 'Москва'},
    {'id': 55512122, 'name': 'Анатолий', 'target_sex': 'female',
     'target_age_min': 18, 'target_age_max': 24, 'target_city': 'Санкт-Петербург'},
    # {'id': 55512123, 'name': 'Андрей', 'target_sex': 'female',
    #  'target_age_min': 16, 'target_age_max': 18, 'target_city': 'Москва'},
    # {'id': 55512124, 'name': 'Наталья'},
    {'id': 55512125, 'name': 'Ипполит', 'target_sex': 'female',
     'target_age_min': 30, 'target_age_max': 35, 'target_city': 'Казань'}
]

favorites = [
    {'id': 55500111, 'name': 'Марья', 'surname': 'Болконская', 'profile_link': 'https://vk.com/id55500111'},
    {'id': 55500112, 'name': 'Елена', 'surname': 'Курагина', 'profile_link': 'https://vk.com/id55500112'},
    {'id': 55500113, 'name': 'Пётр', 'surname': 'Безухов', 'profile_link': 'https://vk.com/id55500113'},
    {'id': 55512124, 'name': 'Наталья', 'surname': 'Ростова', 'profile_link': 'https://vk.com/id55512124'}
]

# photos(
#             favorites_id INTEGER NOT NULL REFERENCES favorites(id),
#             photo_1 BYTEA,
#             photo_2 BYTEA,
#             photo_3 BYTEA
# user_favorite(
#             user_id INTEGER NOT NULL REFERENCES users(id),
#             favorite_id INTEGER NOT NULL REFERENCES favorites(id),
#             is_banned BOOLEAN DEFAULT FALSE,
#             PRIMARY KEY (user_id, favorite_id)


def some_func(**kwargs):
    [print(kwargs[x]) for x in ['id', 'name', 'target_sex', 'target_age_min', 'target_age_max', 'target_city']]


# for u in users:
#     some_func(**u)
