import os, vk_api
from vkbottle.bot import Message, Bot
from vkbottle import BaseStateGroup, CtxStorage
from database.database_methods import *
from card_creation import Create
from action import action_bot, action_card


class State(BaseStateGroup):
     CITY = 1
     SEX = 2
     AGE = 3 
     END = 4
     CITY_EDIT = ''
     AGE_EDIT = ''
     SEX_EDIT = ''

class handlers_start:

    def __init__(self) -> None:
        self.action_bot = action_bot()
        self.action_card = action_card()
        self.bot = Bot(os.getenv('vkinder'))
        self.create = Create()
        self.states = State
        self.ctx = CtxStorage()

        #Начало регестрации пользователя в приложении vkinder
        @self.bot.on.message(lev="Начать")
        async def start(message: Message):
            if get_user_info(message.peer_id) != None:
                return "Вы уже прошли регестрацию\n Для редактирования данных перейдите по кнопке изменить данные"
            user_info = await self.bot.api.users.get(message.from_id)
            first_name = user_info[0].first_name
            await message.answer("Доброго времени суток, {}".format(first_name))
            self.ctx.set("name", first_name)
            self.ctx.set("id", message.from_id)
            await self.bot.state_dispenser.set(message.peer_id, self.states.CITY)
            return "Укажите город в котором проживаете"
        
        @self.bot.on.message(state=self.states.CITY)
        async def city(message: Message):
            if len(message.text.split()) != 1:
                await self.bot.state_dispenser.set(message.peer_id, self.states.CITY)
                return "Вы не верно ввели город"
            self.ctx.set("city", message.text)
            await self.bot.state_dispenser.set(message.peer_id, self.states.SEX)
            return "Укажите свой пол м/ж"
        
        # #Сохраняем пол который ввёл пользователь
        @self.bot.on.message(state=self.states.SEX)
        async def sex(message:Message):
            if message.text not in ["м","ж"]:
                await self.bot.state_dispenser.set(message.peer_id, self.states.SEX)
                return "Вы не верно ввели пол"
            self.ctx.set("sex", message.text)
            await self.bot.state_dispenser.set(message.peer_id, self.states.AGE)
            return "Укажите свой возрост"
        
        # #Сохраняем возраст который ввёл пользователь и заносим данные в БД
        # #И выводим кнопки для дальнейшего пользования
        @self.bot.on.message(state = self.states.AGE)
        async def age(message:Message):
            if message.text.isdigit() == False :
                await self.bot.state_dispenser.set(message.peer_id, self.states.AGE)
                return "Вы не верно ввели возраст"
            self.ctx.set("age", message.text)
            name = self.ctx.get("name")
            _age = self.ctx.get("age")
            _city = self.ctx.get("city")
            _sex = self.ctx.get("sex")
            id = self.ctx.get("id")
            if _sex == "м":
                await add_user(id, name, "male", int(_age) - 3, int(_age) + 3, _city)
            elif _sex == "ж":
                await add_user(id, name, "female", int(_age) - 3, int(_age) + 3, _city)
            keyboard = await self.create.keyboard("start")
            await self.bot.state_dispenser.delete(message.peer_id)
            await message.answer(
                                f"Проверка данныx \n Имя: {name}\n Город:{_city}\n Пол:{_sex}\n Возраст:{_age}",
                                keyboard=keyboard
                                )
            
        @self.bot.on.message(text = "Главное меню")
        async def main_menu(message: Message):
            keyboard = await self.create.keyboard(message.text)
            await message.answer(
                                "Перешли в главное меню",
                                keyboard=keyboard
                                )
        #Начинаем поиск людей по критериям
        @self.bot.on.message(text="Начать знакомства")
        async def start(message: Message):
            matched = await self.action_bot.start_search(message)
            owner_id = matched.pop(0)
            user_info = await self.action_bot.search_user_info(owner_id)
            self.ctx.set("matched", matched)
            previous = []
            now = [owner_id]
            self.ctx.set('now', now)
            self.ctx.set('previous', previous)
            photos = await self.action_bot.search_max_like_fotos(owner_id)
            self.bot.state_dispenser.set("photos", photos)
            kb = await self.create.keyboard(message.text)
            user_info = await self.action_bot.search_user_info(owner_id)
            await message.answer(attachment=photos[0])
            await message.answer(
                                user_info, 
                                keyboard=kb
                                )
            
        @self.bot.on.message(text="Продолжить знакомства")
        async def go_on(message: Message):
            matched = self.ctx.get("matched")
            print(matched)
            
        @self.bot.on.message(text="Следущий")
        async def next_user(message: Message):
            now = (self.ctx.get('now'))
            previous = (self.ctx.get('previous'))
            old_owner_id = now.pop(0)
            previous.append(old_owner_id)
            self.ctx.set('previous', previous)
            matched = self.ctx.get('matched')
            owner_id = matched.pop(0)
            now.append(owner_id)
            self.ctx.set('now', now)
            self.ctx.set('matched', matched)
            user_info = await self.action_bot.search_user_info(owner_id)
            photos = (await self.action_bot.search_max_like_fotos(owner_id))
            self.bot.state_dispenser.set("photos", photos)
            kb = await self.create.keyboard(message.text)
            print(user_info, photos[1])
            await message.answer(attachment=photos[0])
            await message.answer(
                                user_info, 
                                keyboard=kb
                                )
            
        @self.bot.on.message(text="Предыдущий")
        async def previous_user(message: Message):
            now = self.ctx.get('now')
            previous = self.ctx.get('previous')
            matched = self.ctx.get('matched')
            old_owner_id = now.pop(0)
            matched.insert(0, old_owner_id)
            owner_id = previous.pop(-1)
            now.append(owner_id)
            self.ctx.set('now', now)
            self.ctx.set('matched', matched)
            self.ctx.set('previous',previous)
            user_info = await self.action_bot.search_user_info(owner_id)
            photos = await self.action_bot.search_max_like_fotos(owner_id)
            self.bot.state_dispenser.set("photos", photos)
            kb = self.create.keyboard(message.text)
            await message.answer(attachment=photos[0])
            await message.answer(
                                user_info, 
                                keyboard=kb
                                )
            
        @self.bot.on.message(text="❤")
        async def like_users(message: Message):
            favorite_id = (await self.ctx.get('now'))[0]
            photos = self.bot.state_dispenser.get('photos')
            await add_user_favorite(message.peer_id, favorite_id, False)
            # await add_photos(favorite_id, photos[0], photos[1], photos[2])

        @self.bot.on.message(text="🚫")
        async def black_list_users(message:Message):
            await message.answer(
                                "Кнопка не работает"
                                )
            # now =  self.ctx.get('now')
            # favorite_id = now.pop(0)
            # await send_to_blacklist(message.peer_id, favorite_id, True)
            # await message.answer("Пользователь добавлен в чёрный список")
            # matched = self.ctx.get('matched')
            # owner_id = matched.pop(0)
            # now.append(owner_id)
            # self.ctx.set('matched', matched)
            # self.ctx.set('now', now)
            # user_info = await self.action_bot.search_user_info(owner_id)
            # photos = await self.action_bot.search_max_like_fotos(owner_id)
            # kb = self.create.keyboard(message.text)
            # await message.answer(attachment=photos[0])
            # await message.answer(
            #                     user_info, 
            #                     keyboard=kb
            #                     )
            
        @self.bot.on.message(text="Понравившиеся")
        async def like_users(message: Message):
            await get_favorite_info()

        @self.bot.on.message(text="Чёрный список")
        async def black_list_users(message:Message):
            await message.answer("Кнопка не работает")
            
        @self.bot.on.message(text = "Изменить данные")
        async def change_data(message: Message):
            keyboard = await self.create.keyboard(message.text)
            await message.answer('Какие данные хотите изменить?', keyboard=keyboard)

        @self.bot.on.message(lev = "Город")
        async def city_edit_state(message: Message):
            await message.answer("Кнопка не работает")
            # await self.bot.state_dispenser.set(message.peer_id, self.states.CITY_EDIT)

        
        @self.bot.on.message(state=self.states.CITY_EDIT)
        async def city_edit(message: Message):
            if len(message.text.split()) != 1:
                await self.bot.state_dispenser.set(message.peer_id, self.states.CITY_EDIT)
                return "Вы не верно ввели город"
            await self.bot.state_dispenser.delete(message.peer_id)
            await message.answer("Данные успешно изменены")
            

        @self.bot.on.message(lev = "Возраст")
        async def age_edit_state(message: Message):
            await message.answer("Кнопка не работает")
            # await self.bot.state_dispenser.set(message.peer_id, self.states.AGE_EDIT)

        @self.bot.on.message(state=self.states.AGE_EDIT)
        async def age_edit(message: Message):
            if message.text.isdigit() == False :
                await self.bot.state_dispenser.set(message.peer_id, self.states.AGE_EDIT)
                return "Вы не верно ввели возраст"
            await self.bot.state_dispenser.delete(message.peer_id)
            await message.answer("Данные успешно изменены")
        
        @self.bot.on.message(lev = "Пол")
        async def sex_edit_state(message: Message):
            await message.answer("Кнопка не работает")
            # await self.bot.state_dispenser.set(message.peer_id, self.states.SEX_EDIT)
        
        @self.bot.on.message(state = self.states.SEX_EDIT)
        async def sex_edit(message: Message):
            if message.text not in ["м","ж"]:
                await self.bot.state_dispenser.set(message.peer_id, self.states.SEX)
                return "Вы не верно ввели пол"
            await self.bot.state_dispenser.delete(message.peer_id)
            await message.answer("Данные успешно изменены")