from vkbottle import API, Keyboard, KeyboardButtonColor, Text, PhotoMessageUploader
from vkbottle.bot import Bot, Message
# Класс для создания карточки
class Create:

    def __init__(self) -> None:
        self.secondary = KeyboardButtonColor.SECONDARY

    # Создание кнопок для карточки
    def keyboard(self, *args):
        if args[0] == "Начать":
            keyboard = Keyboard(one_time = True, inline = False)
            keyboard.add(Text("Поехали!"), color = self.secondary)
            keyboard.row()
            keyboard.add(Text("Понравившиеся"), color = self.secondary)
            keyboard.add(Text("Чёрный список"), color = self.secondary)
            return keyboard

    # Создание фото для карточки
    def foto(self):
        pass

    # Сборка карточки
    def card_assembly(self):
        pass