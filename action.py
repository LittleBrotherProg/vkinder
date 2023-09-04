# import os
from vkbottle import API
from database.get import *


class ActionBot:

    def __init__(self) -> None:
        self.api = API(os.getenv('USERVK'))

    # Поиск людей по критериям
    async def start_search(self, message) -> dict:
        user_info = (await get_user_info(message.from_id))[0]
        matched = (await self.api.users.search(
            age_from=user_info['target_age_min'],
            age_to=user_info['target_age_max'],
            hometown=user_info['target_city'],
            count=1000
        )).items
        black_list = await get_black_list(message.peer_id)
        id_matched = [info_user.id for info_user in matched if info_user.is_closed is False if
                      info_user.id not in black_list]
        return id_matched

    async def search_max_like_photos(self, owner_id):
        all_photo = {}
        albums_info = (await self.api.photos.get_albums(
            owner_id=owner_id,
            need_system=1,
            extended=1
        )).items

        id_albums = [album.id for album in albums_info]
        for id_album in id_albums:
            if id_album == -9000:
                photos_info = (await self.api.photos.get_user_photos(
                    user_id=owner_id,
                    extended=1
                )).items
            else:
                photos_info = (await self.api.photos.get(
                    owner_id=owner_id,
                    album_id=id_album,
                    extended=1
                )).items
            for photo in photos_info:
                name_photo = f"photo{owner_id}_{photo.id}"
                like = photo.likes.count
                all_photo[like] = name_photo

        key_max_like = sorted(all_photo)[-3:]
        photos = []
        for id in range(len(key_max_like) - 1, -1, -1):
            photos.append(all_photo.get(key_max_like[id]))

        return photos

    async def search_user_info(self, **params):
        owner_id = params.get("owner_id")
        user_info = (await self.api.users.get(
                                        user_ids=owner_id,
                                        fields="home_town, sex, about"
                                        ))[0]
        # if user_info.is_closed == True:
        #      return 'private'
        first_name = user_info.first_name
        last_name = user_info.last_name
        home_town = user_info.home_town
        about = user_info.about
        # sex = user_info.sex
        link = f"https://vk.com/id{owner_id}"
        if params.get("status") in ["like", "black"]:
            return [owner_id, first_name, last_name, link]
        if about != '':
            user_info = f"{first_name} {last_name}\n Город:{home_town}\n О себе:{about}\n  Ссылка на профиль: {link}"
            return user_info
        about = "*"
        user_info = f"{first_name} {last_name}\n Город:{home_town}\n О себе:{about}\n  Ссылка на профиль: {link}"
        return user_info

    async def check_city(self, city):
        city_all = (await self.api.database.get_cities(country_id=1,
                                                       q=city
                                                       )).items
        one = [city.title for city in city_all]
        if city in one:
            return city
        similar_cities = [city.title for city in city_all if len(str(city.id)) <= 2]
        return similar_cities


# Класс действий с карточкой
class ActionCard:

    def __init__(self):
        pass

    # Переключить на следующую карточку
    def next_card(self):
        pass

    # Переключить на предыдущую карточку
    def previous_card(self):
        pass

    # добавить карточку в фавориты
    def like_card(self):
        pass

    # добавить карточку в чёрный список
    def black_list_card(self):
        pass


class ActionMainMenu:

    def __init__(self) -> None:
        pass

    # Открыть карточки фаворитов
    def open_card_favorites(self):
        pass

    # Открыть карточки из чёрного списка
    def open_card_black_list(self):
        pass

    # Открыть карточки 
    def open_card(self):
        pass
