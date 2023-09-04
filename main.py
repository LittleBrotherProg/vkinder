from handlers import HandlersStart


class VK:

    def __init__(self):
        handlers = HandlersStart()
        self.bot = handlers.bot

    def start_up(self):
        self.bot.run_forever()


if __name__ == "__main__":
    vk_method = VK()
    vk_method.start_up()
