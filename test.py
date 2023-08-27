# import vk_api
import os
# import json
 
# login = ''
# passw = ''
 
# VK = vk_api.VkApi(token=os.getenv('USERVK'))
# VK.auth()
# VK = VK.get_api()

import vk_api

api = vk_api.VkApi(token=os.getenv('USERVK')).get_api()
api = vk.get_api()

AGE_FROM = 16
AGE_TO = 50
CITY = 10

rs = api.users.search(age_from=AGE_FROM, age_to=AGE_TO, count = 100)
# {'count': 1151606, 'items': [{'id': 140182251, 'first_name': ...

users_ids = [user['id'] for user in rs['items']]
print(users_ids)