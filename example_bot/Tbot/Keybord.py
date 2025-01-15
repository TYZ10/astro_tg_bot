from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardButton,
                                    ReplyKeyboardBuilder,
                                    KeyboardButton)
from aiogram import types

from example_bot.Config_bot import ConfigBot


class KeyboardBot:
    def __init__(self, config: ConfigBot):
        pass

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

        return keyboard.as_markup()

