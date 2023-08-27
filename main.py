from vkbottle import API, Keyboard, KeyboardButtonColor, Text, PhotoMessageUploader
from vkbottle.bot import Bot, Message
from time import sleep
from card_creation import Create
import os
from database.database_methods import *
from vkbottle import BaseStateGroup, CtxStorage
import vk_api

# client_id = 51736254

class vk:
     
     def __init__(self, api_token):
          self.bot = Bot(api_token)
          self.create = Create()
          self.states = State
          self.ctx = CtxStorage()
          api = vk_api.VkApi(token=os.getenv('USERVK')).get_api()

          #Начало регестрации пользователя в приложении vkinder
          @self.bot.on.message(lev="Начать")
          async def start(message: Message):
               user_info = await self.bot.api.users.get(message.from_id)
               first_name = user_info[0].first_name
               await message.answer("Доброго времени суток, {}".format(first_name))
               self.ctx.set("name", first_name)
               self.ctx.set("id", message.from_id)
               sleep(1)
               await self.bot.state_dispenser.set(message.peer_id, self.states.CITY)
               return "Укажите город в котором проживаете"
          
          # #Сохраняем город который ввёл пользователь
          @self.bot.on.message(state=self.states.CITY)
          async def city(message: Message):
               self.ctx.set("city", message.text)
               await self.bot.state_dispenser.set(message.peer_id, self.states.SEX)
               return "Укажите свой пол м/ж"
          
          # #Сохраняем пол который ввёл пользователь
          @self.bot.on.message(state=self.states.SEX)
          async def sex(message:Message):
               self.ctx.set("sex", message.text)
               await self.bot.state_dispenser.set(message.peer_id, self.states.AGE)
               return "Укажите свой возрост"
          
          # #Сохраняем возраст который ввёл пользователь и заносим данные в БД
          # #И выводим кнопки для дальнейшего пользования
          @self.bot.on.message(state = self.states.AGE)
          async def age(message:Message):
               self.ctx.set("age", message.text)
               name = self.ctx.get("name")
               _age = self.ctx.get("age")
               _city = self.ctx.get("city")
               _sex = self.ctx.get("sex")
               id = self.ctx.get("id")
               keyboard = self.create.keyboard("start")
               add_user(id, name, _sex, int(_age) - 3, int(_age) + 3, _city)
               await message.answer(
                                    f"Проверка данныx \n Имя: {name}\n Город:{_city}\n Пол:{_sex}\n Возраст:{_age}",
                                    keyboard=keyboard
                                    )
          

          
          @self.bot.on.message(text="Начать знакомства")
          async def start(message: Message):
               user_info = get_user_info(message.from_id)
               rs = api.users.search(
                                        age_from = user_info['target_age_min'], 
                                        age_to = user_info['target_age_max'], 
                                        hometown = user_info['target_city'], 
                                        count = 1000
                                    )['items']
               self.ctx.set("next", rs)
               owner_id = rs[0]['id']
               albums_info = api.photos.getAlbums(
                                                  owner_id = owner_id,
                                                  need_system = 1,
                                                  extended =1
                                                  )["items"]
               id_albums = [album["id"] for album in albums_info]
               all_foto = {}
               for id_album in id_albums:
                    fotos_info = api.photos.get(
                                             owner_id = owner_id,
                                             album_id = id_album,
                                             extended = 1
                                          )["items"]
                    for foto in fotos_info:
                         name_foto = f"photo{owner_id}_{foto['id']}"
                         like = foto["likes"]["count"]
                         all_foto[like] = name_foto
               key_max_like = sorted(all_foto)[-3:]
               photos = [all_foto.get(key_max_like[2]),all_foto.get(key_max_like[1]), all_foto.get(key_max_like[0])]
               await message.answer(attachment=photos)
               kb = self.create.keyboard(message.text)
               await message.answer(f"{rs[0]['first_name']} {rs[0]['last_name']}\n Город:-", keyboard=kb)

          @self.bot.on.message(text="Следущий")
          async def start(message: Message):
               next = self.ctx.get("next")
               last = [next.pop(0)]
               self.ctx.set("last",last)
               owner_id = next[0]['id']
               albums_info = api.photos.getAlbums(
                                                  owner_id = owner_id,
                                                  need_system = 1,
                                                  extended =1
                                                  )["items"]
               id_albums = [album["id"] for album in albums_info]
               all_foto = {}
               for id_album in id_albums:
                    fotos_info = api.photos.get(
                                             owner_id = owner_id,
                                             album_id = id_album,
                                             extended = 1
                                          )["items"]
                    for foto in fotos_info:
                         name_foto = f"photo{owner_id}_{foto['id']}"
                         like = foto["likes"]["count"]
                         all_foto[like] = name_foto
               key_max_like = sorted(all_foto)[-3:]
               photos = []
               for id in range(len(key_max_like)):
                    photos.append(all_foto.get(key_max_like[id]))
               await message.answer(attachment=photos)
               kb = self.create.keyboard(message.text)
               await message.answer(f"{next[0]['first_name']} {next[0]['last_name']}\n Город:-", keyboard=kb)               

          

     def start_up(self):
          self.bot.run_forever()

class State(BaseStateGroup):
     CITY = 1
     SEX = 2
     AGE = 3




if __name__ == "__main__":
     vk_metod = vk(os.getenv('vkinder')) 
     vk_metod.start_up()
