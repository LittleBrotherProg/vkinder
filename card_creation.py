from vkbottle import  Keyboard, KeyboardButtonColor, Text, PhotoMessageUploader

# Класс для создания карточки
class Create:

    def __init__(self) -> None:
        self.secondary = KeyboardButtonColor.SECONDARY
        self.status = {
                        "Начать знакомства": "base",
                        "Понравившиеся": "favorites",
                        "💔": "revome_favorites",
                        "Следующий": "favorites"
                      }

    # Создание кнопок для карточки
    async def keyboard(self, **params):
        keyboard = Keyboard(one_time = False, inline = False)
        if params["indefication"] == "sity":
            for index, sity in enumerate(params["sity"]):
                if (index + 1) % 4 == 0:
                    keyboard.row
                    keyboard.add(
                                Text(sity), 
                                color = self.secondary
                                )
                else:
                    keyboard.add(
                                Text(sity), 
                                color = self.secondary
                                )
            return keyboard
        elif params["indefication"] in ["start", "Главное меню"]:
            if params["indefication"] == "Главное меню":
                # keyboard.add(Text("Продолжить знакомства"), color = self.secondary)
                keyboard.add(
                                Text("Начать знакомства"), 
                                color = self.secondary
                            )
            else:
                keyboard.add(
                                Text("Начать знакомства"), 
                                color = self.secondary
                            )
            keyboard.row()
            keyboard.add(
                            Text("Понравившиеся"), 
                            color = self.secondary
                        )
            keyboard.add(
                            Text("Чёрный список"), 
                            color = self.secondary
                        )
            keyboard.row()
            keyboard.add(
                            Text("Изменить данные"), 
                            color=self.secondary
                        )
            return keyboard
        
        elif params["indefication"] in ["Начать знакомства", "Понравившиеся", "💔", "Следующий"]:
            if params["button_status"] == "favorites":
                status = params["button_status"]
                keyboard.add(
                                Text(
                                        "Следующий", 
                                        payload={"status":status}
                                    ), 
                                color = self.secondary
                            )
            elif params["button_status"] == "last":
                keyboard.add(
                                Text("💔"), 
                                color = self.secondary
                            )
            elif params["button_status"] == "remove_like_last":
                pass
            else:
                status = self.status[f"{params['indefication']}"]
                keyboard.add(
                                Text(
                                        "Следующий", 
                                        payload={"status":status}
                                    ), 
                                color = self.secondary
                            )
            if params["indefication"] == "Понравившиеся" or params["button_status"] == "favorites":
                keyboard.add(
                                Text("💔"), 
                                color = self.secondary
                            )
            elif params["indefication"] == "Начать знакомства":
                keyboard.row()
                keyboard.add(
                                Text("❤"), 
                                color = self.secondary
                            )
                keyboard.add(
                                Text("🚫"), 
                                color = self.secondary
                            )
            keyboard.row()
            keyboard.add(
                            Text("Главное меню"), 
                            color = self.secondary
                        )
            return keyboard
        
        elif params["indefication"] == "Изменить данные":
            keyboard.add(
                            Text("Город"), 
                            color = self.secondary
                        )
            keyboard.add(
                            Text("Возраст"), 
                            color = self.secondary
                        )
            keyboard.add(
                            Text("Пол"), 
                            color = self.secondary
                        )
            keyboard.row()
            keyboard.add(Text("Главное меню"), color = self.secondary)
            return keyboard