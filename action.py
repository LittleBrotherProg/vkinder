import os
from database.database_methods import *
# from vkbottle.api import API
from vkbottle import API
from vkbottle.exception_factory.base_exceptions import VKAPIError 


class action_bot:

    def __init__(self) -> None:
        self.api = API(os.getenv('USERVK'))
    
    #Поиск людей по критериям
    async def start_search(self, message) -> dict:
        user_info = await get_user_info(message.from_id)
        matched = (await self.api.users.search(
                                        age_from = user_info['target_age_min'], 
                                        age_to = user_info['target_age_max'], 
                                        hometown = user_info['target_city'], 
                                        count = 1000
                                        )).items
        id_matched = [info_user.id for info_user in matched if info_user.is_closed == False]
        return id_matched
    
    async def search_max_like_fotos(self, owner_id):
            all_foto = {}
            albums_info = (await self.api.photos.get_albums(
                                                            owner_id = owner_id,
                                                            need_system = 1,
                                                            extended =1
                                                            )).items
            
            id_albums = [album.id for album in albums_info]
            for id_album in id_albums:
                        if id_album == -9000:
                            fotos_info = (await self.api.photos.get_user_photos(
                                                                user_id=owner_id,
                                                                extended = 1
                                                            )).items
                        else:
                            fotos_info = (await self.api.photos.get(
                                                                    owner_id = owner_id,
                                                                    album_id = id_album,
                                                                    extended = 1
                                                                    )).items
                        for foto in fotos_info:
                            name_foto = f"photo{owner_id}_{foto.id}"
                            like = foto.likes.count
                            all_foto[like] = name_foto

            key_max_like = sorted(all_foto)[-3:]
            photos= []
            for id in range(len(key_max_like)-1, -1, -1):
                        photos.append(all_foto.get(key_max_like[id]))

            return [photos, id_albums]

    async def search_user_info(self, **params):
        owner_id = params.get("owner_id")
        user_info = (await self.api.users.get(
                                        user_ids=owner_id,
                                        fields="home_town, sex, about"
                                        ))[0]
        if user_info.is_closed == True:
             return 'private'
        first_name = user_info.first_name
        last_name = user_info.last_name
        home_town = user_info.home_town
        about = user_info.about
        sex = user_info.sex
        link = f"https://vk.com/id{owner_id}"
        if params.get("status") == "like":
             return [owner_id ,first_name, last_name, link]
        if about != '':
            user_info = f"{first_name} {last_name}\n Город:{home_town}\n О себе:{about}\n Пол:{sex}\n Сылка на профиль: {link}"
            return user_info
        about = "*"
        user_info = f"{first_name} {last_name}\n Город:{home_town}\n О себе:{about}\n Пол:{sex}\n Сылка на профиль: {link}"
        return user_info


# Класс действий с карточкой
class action_card():

    def __init__(self):
       pass

    # Переключить на следущую картчоку
    def next_card(self):
        pass

    # Переключить на предыдущую картчоку
    def previous_card(self):
        pass

    # добавить карточку в фавориты
    def like_card(self):
        pass

    # добавить карточку в чёрный список
    def black_list_card(self):
        pass

                 

class action_main_menu:

    def __init__(self) -> None:
        pass

    # Открыть карточки фаворитов
    def open_card_favorits(self):
        pass

    # Открыть карточки из чёрного списка
    def open_card_black_list(self):
        pass

    # Открыть карточки 
    def open_card(self):
        pass