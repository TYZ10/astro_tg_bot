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
        self.subscribe_ikb = subscribe_ikb.as_markup()

        # self.main_menu_kb = self.__reply_kb(
        #     [
        #         "💳 Оплата подписки",
        #         "🪐 Анализ натальной карты",
        #         "☀️ Прогнозы",
        #         "🎁 Реферальная система",
        #         "⚙️ Изменить данные",
        #         "❓ Помощь",
        #         "💼 Бизнес-гороскоп",
        #         "🚀 Рекомендации по самореализации",
        #         "💞 Анализ совместимости в отношениях",
        #         "❤️‍🩹 Астрологический прогноз для здоровья",
        #         "✨ Анализ сильных сторон личности",
        #     ],
        #     adjust_count=2
        # )

        self.main_menu_kb = self.__reply_kb(
            [
                "🔮 Анализ натальной карты",
                "🌟 Прогнозы и гороскопы",
                "💞 Анализ совместимости в отношениях",
                "☀️ Ежедневные прогнозы",
                "❓ Помощь",
            ],
            adjust_count=2
        )

        self.natal_card_menu_ikb = self.__inline_kb(
            {
                "🪐 Анализ натальной карты": "🪐 Анализ натальной карты",
                "✨ Анализ сильных сторон личности":
                    "✨ Анализ сильных сторон личности",
                "🚀 Рекомендации по самореализации":
                    "🚀 Рекомендации по самореализации",
            }
        )

        self.predictions_and_horoscopes_ikb = self.__inline_kb(
            {
                "🗓 Прогноз на текущий год": "select prediction_year",
                "🗓 Прогноз на следующий год": "select prediction_year n",
                "📆 Прогноз на следующий месяц": "select prediction_month n",
                "📆 Прогноз на текущий месяц": "select prediction_month",
                "💼 Бизнес-гороскоп": "💼 Бизнес-гороскоп",
                "❤️‍🩹 Астрологический прогноз для здоровья":
                    "Прогноз для здоровья",
                "☀️ Ежедневные прогнозы": "select prediction_day",
            }
        )

        self.daily_forecasts_ikb = self.__inline_kb(
            {
                "💳 Оплата подписки": "payments",
                "🎁 Реферальная система": "🎁 Реферальная система",
                "⚙️ Изменить данные": "⚙️ Изменить данные",
            }
        )

        self.my_data_ikb = self.__inline_kb(
            {
                "Изменить свои данные": "modify my data",
                "Изменить время авто предсказания": "set time prediction",
                "Главное меню": "main menu"
            }
        )

        self.abolition_ikb = self.__inline_kb(
            {
                "Отменить ввод данных": "main menu"
            }
        )

        self.start_generation_ikb = self.__inline_kb(
            {
                "📂 Использовать предыдущие данные": "start generation",
                "✍️ Ввести новые данные": "modify my data",
                "❌ Отменить генерацию": "main menu",
            }
        )

        self.selection_predictions_ikb = self.__inline_kb(
            {
                "На год": "select prediction_year",
                "На месяц": "select prediction_month",
                "На день (Требует платной подписки!)": "select prediction_day",
                "Отмена": "main menu",
            }
        )

        self.get_aspect_selection_ikb = self.__inline_kb(
            {
                "Финансы и карьера": "Финансы и карьера",
                "Семья и дети": "Семья и дети",
                "Любовь и отношения": "Любовь и отношения",
                "Духовный рост и саморазвитие": "Духовный рост и саморазвитие",
                "Здоровье и энергия": "Здоровье и энергия",
                "Опасности и предупреждения": "Опасности и предупреждения",
                "Дети и воспитание": "Дети и воспитание",
                "Миссия и предназначение": "Миссия и предназначение",
            },
            adjust_count=2
        )

        self.payments_ikb = self.__inline_kb(
            {
                "Продлить подписку": "payments",
                "Главное меню": "main menu",
            }
        )

        self.ref_payments_ikb = self.__inline_kb(
            {
                "Да": "ref payments",
                "Нет": "main menu",
            }
        )
        self.no_generation_data_ikb = self.__inline_kb(
            {
                "Ввести данные.": "modify my data",
                "Главное меню.": "main menu",
            }
        )
        self.payments_choice_ikb = self.__inline_kb(
            {
                "Оплатить рублями": "choice payments_rub",
                "Оплатить реферальными баллами": "choice payments_point",
                "Назад": "main menu",
            }
        )

    def create_payments_ikb(self, url, id):
        kb_payment = InlineKeyboardBuilder()
        kb_payment.button(text="Оплатить", url=url)
        kb_payment.button(text="Проверить оплату",
                          callback_data=f"check payment_{id}")
        kb_payment.button(text="Отменить оплату",
                          callback_data="main menu")
        kb_payment.adjust(1)
        return kb_payment.as_markup()

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

