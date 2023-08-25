<<<<<<< HEAD
import os 
import asyncio
from vkbottle.bot import Bot, Message
from time import sleep
from card_creation import Create
=======
import vk_api.vk_api, json

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
>>>>>>> 82e953186caffef7138f76ede79de068c9acffaf

class vk:
     
     def __init__(self, api_token):
          self.bot = Bot(api_token)
          self.create = Create()



          @self.bot.on.message(text="Начать")
          async def start(message: Message):
               user_info = await self.bot.api.users.get(message.from_id)
               # keyboard = Keyboard(one_time=False, inline=False)
               # keyboard.add(Text("Предыдуший"), color=KeyboardButtonColor.PRIMARY)
               # keyboard.add(Text("Следующий"), color=KeyboardButtonColor.NEGATIVE)
               # keyboard.row()
               # keyboard.add(Text("❤"), color=KeyboardButtonColor.SECONDARY)
               # keyboard.add(Text("🚫"), color=KeyboardButtonColor.SECONDARY)
               # photo = 'photo405415109_457240825'
               # await message.answer("Доброго времени суток, {}".format(user_info[0].first_name), keyboard=keyboard, attachment=photo)
               await message.answer("Доброго времени суток, {}".format(user_info[0].first_name))
               sleep(1)
               keboard = self.create.keyboard(message.text)
               sleep(1)
               await message.answer("Начнём знакомства?", keyboard=keboard)
               
          @self.bot.on.message(text="Поехали!")
          async def start(message: Message):
               user_info = await self.bot.api.users.get(message.from_id)
               card = self.create.card_assembly(message.text)
               await message.answer("Привет, {}".format(user_info[0].first_name))
          

     def start_up(self):
          self.bot.run_forever()



if __name__ == "__main__":
<<<<<<< HEAD
     # vk_metod = vk(os.getenv('vkinder'), 222142527)
     vk_metod = vk(os.getenv('vkinder')) 
     vk_metod.start_up()
=======
     vk_metod = vk(token, 222142527) 
     vk_metod.send_message(422264572, "Некст")
>>>>>>> 82e953186caffef7138f76ede79de068c9acffaf
