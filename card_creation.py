from vkbottle import API, Keyboard, KeyboardButtonColor, Text, PhotoMessageUploader
from vkbottle.bot import Bot, Message
# Класс для создания карточки
class Create:

    def __init__(self) -> None:
        self.secondary = KeyboardButtonColor.SECONDARY

    # Создание кнопок для карточки
    async def keyboard(self, indefication):
        if indefication in ["start", "Главное меню"]:
            keyboard = Keyboard(one_time = False, inline = False)
            if indefication == "Главное меню":
                # keyboard.add(Text("Продолжить знакомства"), color = self.secondary)
                keyboard.add(Text("Начать знакомства"), color = self.secondary)
            else:
                keyboard.add(Text("Начать знакомства"), color = self.secondary)
            keyboard.row()
            keyboard.add(Text("Понравившиеся"), color = self.secondary)
            keyboard.add(Text("Чёрный список"), color = self.secondary)
            keyboard.row()
            keyboard.add(Text("Изменить данные"), color=self.secondary)
            return keyboard
        
        elif indefication in ["Начать знакомства", "Понравившиеся"]:
            keyboard = Keyboard(one_time = False, inline = False)
            # keyboard.add(Text("Предыдущий"), color = self.secondary)
            if indefication == "Понравившиеся":
                keyboard.add(Text("Следущий", payload={"status":"favorites"}), color = self.secondary)
                keyboard.add(Text("💔"), color = self.secondary)
                keyboard.row()
            else:
                keyboard.add(Text("Следущий", payload = {"status":"base"}), color = self.secondary)
                keyboard.row()
                keyboard.add(Text("❤"), color = self.secondary)
                keyboard.add(Text("🚫"), color = self.secondary)
                keyboard.row()
            keyboard.add(Text("Главное меню"), color = self.secondary)
            return keyboard
        
        elif indefication == "Изменить данные":
            keyboard = Keyboard(one_time = False, inline = False)
            keyboard.add(Text("Город"), color = self.secondary)
            keyboard.add(Text("Возраст"), color = self.secondary)
            keyboard.add(Text("Пол"), color = self.secondary)
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