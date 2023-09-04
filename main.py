from handlers import handlers_start

class vk:
     
     def __init__(self):
          handlers = handlers_start()
          self.bot = handlers.bot

     def start_up(self):
          self.bot.run_forever()


if __name__ == "__main__":
     vk_metod = vk()  
     vk_metod.start_up()
