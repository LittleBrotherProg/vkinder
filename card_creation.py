from vkbottle import API, Keyboard, KeyboardButtonColor, Text, PhotoMessageUploader
from vkbottle.bot import Bot, Message
# Класс для создания карточки
class Create:

    def __init__(self) -> None:
        self.secondary = KeyboardButtonColor.SECONDARY

    # Создание кнопок для карточки
    def keyboard(self, indefication):
        if indefication == "start":
            keyboard = Keyboard(one_time = False, inline = False)
            keyboard.add(Text("Начать знакомства"), color = self.secondary)
            keyboard.row()
            keyboard.add(Text("Понравившиеся"), color = self.secondary)
            keyboard.add(Text("Чёрный список"), color = self.secondary)
            keyboard.row()
            keyboard.add(Text("Изменить данные"), color=self.secondary)
            return keyboard
        
        elif indefication == "Начать знакомства":
            keyboard = Keyboard(one_time = False, inline = False)
            keyboard.add(Text("Предыдущий"), color = self.secondary)
            keyboard.add(Text("Следущий"), color = self.secondary)
            keyboard.row()
            keyboard.add(Text("Понравившиеся"), color = self.secondary)
            keyboard.add(Text("Чёрный списко"), color = self.secondary)
            keyboard.row()
            keyboard.add(Text("Главное меню"), color = self.secondary)
            return keyboard

    # Создание фото для карточки
    def foto(self):
        pass

    # Сборка карточки
    def card_assembly(self, **params):
        keyboard = self.keyboard()
        foto = []
        firtst_name = str()
        second_name = str()
        return keyboard