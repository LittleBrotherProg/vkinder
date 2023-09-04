# import os
from vkbottle.bot import Message, Bot
from vkbottle import BaseStateGroup, CtxStorage
# from database.add import *
from database.button import *
from database.delete import *
from database.get import *
from database.update import *
from card_creation import Create
from action import ActionBot, ActionCard
import ast


class State(BaseStateGroup):
    CITY = 1
    SEX = 2
    AGE = 3
    END = 4
    CITY_EDIT = ''
    AGE_EDIT = ''
    SEX_EDIT = ''


class HandlersStart:

    def __init__(self) -> None:
        self.action_bot = ActionBot()
        self.action_card = ActionCard()
        self.bot = Bot(os.getenv('vkinder'))
        self.create = Create()
        self.states = State
        self.ctx = CtxStorage()
        self.status = {
            "favorites": [
                get_favorites_viewed_id,
                update_favorite_viewed,
                get_favorite_info,
                delete_favorites_last_viewed
            ],
            "base": [
                get_last_viewed,
                update_viewed,
                self.action_bot.search_user_info
            ],
            "remove_favorites": [
                get_favorites_viewed_id,
                update_favorite_viewed,
                get_favorite_info,
                delete_favorites_last_viewed
            ]
        }

        # Начало регистрации пользователя в приложении vkinder
        @self.bot.on.message(lev="Начать")
        async def start(message: Message):
            if await get_user_info(message.peer_id) != []:
                return "Вы уже прошли регистрацию\n Для редактирования данных перейдите по кнопке изменить данные"
            user_info = await self.bot.api.users.get(message.from_id)
            first_name = user_info[0].first_name
            await message.answer("Доброго времени суток, {}".format(first_name))
            self.ctx.set(
                "name",
                first_name
            )
            self.ctx.set(
                "id",
                message.from_id
            )
            await self.bot.state_dispenser.set(
                message.peer_id,
                self.states.CITY
            )
            return "Укажите город, в котором проживаете"

        @self.bot.on.message(state=self.states.CITY)
        async def city(message: Message):
            city = await self.action_bot.check_city(message.text)
            if type(city) == list:
                await self.bot.state_dispenser.set(
                    message.peer_id,
                    self.states.CITY
                )
                await message.answer("Город, который вы ввели, не найден")
                kb = await self.create.keyboard(
                    identification="city",
                    city=city
                )
                await message.answer(
                    f"Вот что мы смогли найти похожее на {message.text}",
                    keyboard=kb
                )
                return "Напишите или выберите город"
            self.ctx.set("city", message.text)
            await self.bot.state_dispenser.set(
                message.peer_id,
                self.states.SEX
            )
            return "Укажите свой пол м/ж"

        # Сохраняем пол который ввёл пользователь
        @self.bot.on.message(state=self.states.SEX)
        async def sex(message: Message):
            if message.text.lower() not in ["м", "ж"]:
                await self.bot.state_dispenser.set(
                    message.peer_id,
                    self.states.SEX
                )
                return "Вы не верно ввели пол"
            self.ctx.set("sex", message.text)
            await self.bot.state_dispenser.set(
                message.peer_id,
                self.states.AGE
            )
            return "Укажите свой возраст"

        # Сохраняем возраст который ввёл пользователь и заносим данные в БД
        # И выводим кнопки для дальнейшего пользования
        @self.bot.on.message(state=self.states.AGE)
        async def age(message: Message):
            if message.text.isdigit() is False or len(message.text) != 2:
                await self.bot.state_dispenser.set(
                    message.peer_id,
                    self.states.AGE
                )
                return "Вы неверно ввели возраст"
            self.ctx.set("age", message.text)
            name = self.ctx.get("name")
            _age = self.ctx.get("age")
            _city = self.ctx.get("city")
            _sex = self.ctx.get("sex")
            id = self.ctx.get("id")
            # 
            if _sex.lower() == "м":
                await add_record_user_table(
                                            id, 
                                            name, 
                                            True, 
                                            # 
                                            int(_age) - 3, 
                                            int(_age) + 3, 
                                            _city
                                            )
            elif _sex.lower() == "ж":
                await add_record_user_table(
                    id,
                    name,
                    False,
                    int(_age) - 3,
                    int(_age) + 3,
                    _city
                )
            keyboard = await self.create.keyboard(identification="start")
            await self.bot.state_dispenser.delete(message.peer_id)
            await message.answer(
                f"Проверка данныx \n Имя: {name}\n Город:{_city}\n Пол:{_sex}\n Возраст:{_age}",
                keyboard=keyboard
            )

        @self.bot.on.message(text="Главное меню")
        async def main_menu(message: Message):
            keyboard = await self.create.keyboard(identification=message.text)
            await message.answer(
                "Перешли в главное меню",
                keyboard=keyboard
            )

        # Начинаем поиск людей по критериям
        @self.bot.on.message(text="Начать знакомства")
        async def start(message: Message):
            await delete_user_last_viewed(message.peer_id)
            matched = await self.action_bot.start_search(message)

            await add_record_viewed_table(message.peer_id, str(matched))
            owner_id = matched[0]
            photos = await self.action_bot.search_max_like_photos(owner_id)
            kb = await self.create.keyboard(
                identification=message.text,
                button_status="base"
            )
            user_info = await self.action_bot.search_user_info(
                owner_id=owner_id,
                status="search"
            )
            await message.answer(
                user_info,
                keyboard=kb,
                attachment=photos
            )

        @self.bot.on.message(text="Продолжить знакомства")
        async def go_on(message: Message):
            matched = self.ctx.get("matched")
            get_last_viewed
            print(matched)

        # Переключение на следущую карточку
        @self.bot.on.message(text="Следующий")
        async def next_user(message: Message):
            status = ast.literal_eval(message.payload).get("status")
            viewed = self.status.get(status)
            users_list = ast.literal_eval(await viewed[0](message.peer_id))
            if len(users_list) == 0:
                await message.answer(f"Это были все найденые по вашим критериям")
                await viewed[3](message.peer_id)
                return
            elif len(users_list[1:]) == 1:
                await viewed[1](message.peer_id, str(users_list[1:]))
                kb = await self.create.keyboard(
                    identification=message.text,
                    button_status="last"
                )
            else:
                await viewed[1](message.peer_id, str(users_list[1:]))
                kb = await self.create.keyboard(
                    identification=message.text,
                    button_status="favorites"
                )
            if status == "remove_favorites":
                owner_id = users_list[0]
            else:
                owner_id = users_list[1:][0]
            user = await viewed[2](
                owner_id=owner_id,
                status="search"
            )
            if status in ["favorites", "remove_favorites"]:
                photos = [
                    user.get("photo_1"),
                    user.get("photo_2"),
                    user.get("photo_3")
                ]
                await message.answer(
                    f"{user.get('name')} {user.get('surname')}\n {user.get('profile_link')}",
                    keyboard=kb,
                    attachment=photos
                )
                return
            photos = (await self.action_bot.search_max_like_photos(users_list[1:][0]))
            await message.answer(
                user,
                attachment=photos
            )

        # Добавление в понравившиеся
        @self.bot.on.message(text="❤")
        async def like_users(message: Message):
            favorite_id = ast.literal_eval(await get_last_viewed(message.peer_id))[0]
            user_info = await self.action_bot.search_user_info(
                owner_id=favorite_id,
                status="like"
            )
            if await get_favorite_info(owner_id=favorite_id) != []:
                await message.answer(f"{user_info[1]} {user_info[2]} уже в вашем списке понравившихся")
                return
            photos = (await self.action_bot.search_max_like_photos(favorite_id))
            photos_favorites = {}
            for index, photo in enumerate(photos):
                photos_favorites[f"photo_{index + 1}"] = photo
            await add_favorite(
                message.peer_id,
                id=user_info[0],
                name=user_info[1],
                surname=user_info[2],
                profile_link=user_info[3],
                photos=photos_favorites
            )
            await message.answer(f"{user_info[1]} {user_info[2]} успешно добавлен в ваш список понравившихся")

        @self.bot.on.message(text="💔")
        async def delete_favorite(message: Message):
            await message.answer("Кнопка не работает")

        #     favorites_id = ast.literal_eval(await get_favorites_viewed_id(message.peer_id))
        #     if len(favorites_id) == 1:
        #         keyboard = await self.create.keyboard(
        #                                             identification = message.text,
        #                                             button_status = "remove_like_last"
        #                                         )
        #         await message.answer(
        #                             f"{favorite['name']} {favorite['surname']} был(а) удалён(а) из списка понравившихся",
        #                             keyboard = keyboard
        #                         )
        #         await message.answer(f"Это были все найденые по вашим критериям")
        #         await delete_favorites_last_viewed(message.peer_id)
        #         return
        #     favorite_id = favorites_id[0]
        #     await update_favorite_viewed(message.peer_id, str(favorites_id[1:]))
        #     favorite = await get_favorite_info(owner_id = favorite_id)
        #     await delete_favorite_(message.peer_id, favorite_id)
        #     keyboard = await self.create.keyboard(
        #                                             identification = message.text,
        #                                             button_status = "remove_like"
        #                                         )
        #     await message.answer(
        #                             f"{favorite['name']} {favorite['surname']} был(а) удалён(а) из списка понравившихся",
        #                             keyboard = keyboard
        #                         )

        @self.bot.on.message(text="🚫")
        async def black_list_users(message: Message):
            favorite_id = ast.literal_eval(await get_last_viewed(message.peer_id))[0]
            user_info = await self.action_bot.search_user_info(
                owner_id=favorite_id,
                status="black"
            )
            photos = (await self.action_bot.search_max_like_photos(favorite_id))
            photos_favorites = {}
            for index, photo in enumerate(photos):
                photos_favorites[f"photo_{index + 1}"] = photo
            await send_to_blacklist(
                message.peer_id,
                id=user_info[0],
                name=user_info[1],
                surname=user_info[2],
                profile_link=user_info[3],
                photos=photos_favorites
            )
            await message.answer(f"{user_info[1]} {user_info[2]} успешно добавлен в чёрный список")

        @self.bot.on.message(text="Понравившиеся")
        async def like_users(message: Message):
            await delete_favorites_last_viewed(message.peer_id)
            favorites_list = await get_all_favorites(message.peer_id)
            if len(favorites_list) == 0:
                await message.answer(f"Вы перешли к понравившимся людям\n Всего понравившихся {len(favorites_list)}")
                return
            await add_record_favorite_viewed_table(message.peer_id, str(favorites_list))
            await message.answer(f"Вы перешли к понравившимся людям\n Всего понравившихся {len(favorites_list)}")
            favorite_id = favorites_list.pop(0)
            favorite = await get_favorite_info(owner_id=favorite_id)
            photos = [
                favorite.get("photo_1"),
                favorite.get("photo_2"),
                favorite.get("photo_3")
            ]
            kb = await self.create.keyboard(
                identification=message.text,
                button_status=''
            )
            await message.answer(
                f"{favorite.get('name')} {favorite.get('surname')}\n {favorite.get('profile_link')}",
                keyboard=kb,
                attachment=photos
            )

        @self.bot.on.message(text="Чёрный список")
        async def black_list_users(message: Message):
            await message.answer("Кнопка не работает")

        @self.bot.on.message(text="Изменить данные")
        async def change_data(message: Message):
            keyboard = await self.create.keyboard(identification=message.text)
            await message.answer('Какие данные хотите изменить?', keyboard=keyboard)

        @self.bot.on.message(lev="Город")
        async def city_edit_state(message: Message):
            await message.answer("Кнопка не работает")
            # await self.bot.state_dispenser.set(message.peer_id, self.states.CITY_EDIT)
            # update_user_info(id, name, target_sex=None, target_age_min=18, target_age_max=99, target_city=None)

        @self.bot.on.message(state=self.states.CITY_EDIT)
        async def city_edit(message: Message):
            if len(message.text.split()) != 1:
                await self.bot.state_dispenser.set(message.peer_id, self.states.CITY_EDIT)
                return "Вы неверно ввели город"
            await self.bot.state_dispenser.delete(message.peer_id)
            await message.answer("Данные успешно изменены")

        @self.bot.on.message(lev="Возраст")
        async def age_edit_state(message: Message):
            await message.answer("Кнопка не работает")
            # await self.bot.state_dispenser.set(message.peer_id, self.states.AGE_EDIT)

        @self.bot.on.message(state=self.states.AGE_EDIT)
        async def age_edit(message: Message):
            if message.text.isdigit() is False:
                await self.bot.state_dispenser.set(message.peer_id, self.states.AGE_EDIT)
                return "Вы неверно ввели возраст"
            await self.bot.state_dispenser.delete(message.peer_id)
            await message.answer("Данные успешно изменены")

        @self.bot.on.message(lev="Пол")
        async def sex_edit_state(message: Message):
            await message.answer("Кнопка не работает")
            # await self.bot.state_dispenser.set(message.peer_id, self.states.SEX_EDIT)

        @self.bot.on.message(state=self.states.SEX_EDIT)
        async def sex_edit(message: Message):
            if message.text not in ["м", "ж"]:
                await self.bot.state_dispenser.set(message.peer_id, self.states.SEX)
                return "Вы неверно ввели пол"
            await self.bot.state_dispenser.delete(message.peer_id)
            await message.answer("Данные успешно изменены")
