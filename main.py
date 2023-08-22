token = "vk1.a.ZeQBe9qFIPZB39biyWLmQdpSsxZu_6L4yjH-3ujkCP2YdzQVGJwhy7pIkMASS88aS367dlkWfo-nDCTMsZwASMGGEj76t-AB51AH0XVJ41q87XFI-ntv08UNfvzU-MtQkFSpOHV3O7fwqgZIluWQQwi0xWohz5h_fG88YaCe-x9kKhrsoyEzRftDQJeHiVwBeZrNcLnmHdQR5691gPkHJQ"
import vk_api.vk_api, json

from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

class vk:
     
     def __init__(self, api_token, group_id):
          self.token = api_token
          self.group_id = group_id
          self.vk = vk_api.VkApi(token=api_token)
          self.long_poll = VkBotLongPoll(self.vk, group_id)
          self.vk_api = self.vk.get_api()
          pass
     

     def send_message(self, send_id, label):
          # Настройки для обоих клавиатур
          settings = dict(one_time=False, inline=True)
          carousel = {
                    "type": "carousel",
                    "elements": [
                         {    "photo_id": "422264572_457247007",
                              "buttons": [
                                   {
                                   "action": {
                                        "type": "open_link",
                                        "link": "https://vk.com"
                                   },
                                   "color": "secondary",
                                   "action": {"type": "text", "label": "Label"}
                                   }
                              ],
                              "title": "Title",
                              "description": "Description"
                         },
                         {    "photo_id": "422264572_457247007",
                              "buttons": [
                                   {
                                   "action": {
                                        "type": "open_link",
                                        "link": "https://vk.com"
                                   },
                                   "color": "secondary",
                                   "action": {"type": "text", "label": "Label"}
                                   }
                              ],
                              "title": "Title",
                              "description": "Description"
                         },
                         {    "photo_id": "422264572_457247007",
                              "buttons": [
                                   {
                                   "action": {
                                        "type": "open_link",
                                        "link": "https://vk.com"
                                   },
                                   "color": "secondary",
                                   "action": {"type": "text", "label": "Label"}
                                   }
                              ],
                              "title": "Title",
                              "description": "Description"
                         },

                    ]
               }
          self.vk_api.messages.send(peer_id=send_id, message="Привет", random_id = 24, template = json.dumps(carousel))

if __name__ == "__main__":
     vk_metod = vk(token, 222142527) 
     vk_metod.send_message(422264572, "Некст")