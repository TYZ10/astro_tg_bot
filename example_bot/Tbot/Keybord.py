from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardButton,
                                    ReplyKeyboardBuilder,
                                    KeyboardButton)
from aiogram import types

from example_bot.Config_bot import ConfigBot


class KeyboardBot:
    def __init__(self, config: ConfigBot):
        self.config = config

        subscribe_ikb = InlineKeyboardBuilder()
        subscribe_ikb.button(
            text="Канал",
            url=self.config.CHANEL_URL
        )
        self.subscribe_ikb = subscribe_ikb

        self.main_menu_ikb = self.__reply_kb(
            [
                "Анализ натальной карты",
                "Прогнозы",
                "Реферальная система",
                "Мои данные",
                "Помощь",
                "Гороскоп для бизнеса",
                "Рекомендации по самореализации",
                "Анализ совместимости в отношениях",
                "Астрологический прогноз для здоровья",
            ],
            adjust_count=2
        )

    def __inline_kb(
            self,
            kb_data: dict,
            adjust_count: int = 1
    ) -> types.InlineKeyboardMarkup:
        """Создаёт простую инлайн клавиатуру"""

        keyboard = InlineKeyboardBuilder()
        for text, callback_data in kb_data.items():
            keyboard.button(
                text=text,
                callback_data=callback_data
            )
        keyboard.adjust(adjust_count)

        return keyboard.as_markup()

    def __reply_kb(
            self,
            kb_data: list,
            adjust_count: int = 1
    ) -> types.ReplyKeyboardMarkup:
        """Создаёт простую реплай клавиатуру"""

        keyboard = ReplyKeyboardBuilder()
        for text in kb_data:
            keyboard.button(
                text=text
            )
        keyboard.adjust(adjust_count)

        return keyboard.as_markup(resize_keyboard=True)

