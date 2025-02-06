from datetime import datetime, timedelta

from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from example_bot.misc.datetime_function import get_day_and_hours_from_date

from example_bot.Tbot import BasicBotOperation
from example_bot.Tbot import states


class SetPredictions(BasicBotOperation):
    from example_bot.Tbot.apsheduler import ApshedulerBot

    def __init__(self, config, operation_db, keyboard,
                 apscheduler: ApshedulerBot):
        super().__init__(config, operation_db, keyboard)
        self.apscheduler = apscheduler

    async def start_prediction(
            self,
            message: types.Message,
            state: FSMContext,
    ):
        payments_end = self.operation_db.select_user_info_db(
            self.operation_db.COLUMNS_INFO.payments_end,
            message.from_user.id
        )

        if get_day_and_hours_from_date(payments_end, get_hour=True) == 0:
            return

        text = """☀️ Хочешь начинать каждый день с подсказок от звёзд? Ежедневный гороскоп составляется специально для тебя и приходит вечером в удобное время, которое ты выбираешь. Ты можешь выбрать до 4 сфер, которые для тебя наиболее важны:
💼 Финансы и карьера
👨‍👩‍👧‍👦 Семья и дети
❤️ Любовь и отношения
🌟 Духовный рост и саморазвитие
🏥 Здоровье и энергия
⚠️ Опасности и предупреждения
👶 Дети и воспитание
✨ Миссия и предназначение

Ежедневный гороскоп доступен по подписке. Ты можешь её оформить:
✨ За 2 приглашённых друзей, которые сделают хотя бы одну генерацию.
✨ Или за символическую плату всего 150 рублей — это поможет поддерживать работу бота и оплачивать необходимые сервисы.

Звёзды готовы раскрыть свои тайны! Жми кнопку и начни получать свои прогнозы каждый день. 🚀"""

        await state.set_state(states.predictions_1_aspect)

        await state.update_data(period="day")

        await message.answer(
            text=text,
            reply_markup=self.keyboard.get_aspect_selection_ikb
        )

    async def set_prediction(
            self,
            message: types.Message,
            state: FSMContext):

        set_time = message.text
        try:
            set_time = datetime.strptime(set_time, '%H %M').time()
        except:
            await message.answer(
                text=("Введён неверный формат времени."
                      "Введите время рождения в "
                      "формате HH MM (Часы минуты) числами!\n\n"
                      "Пример: 12 30"),
                reply_markup=self.keyboard.abolition_ikb)
            return

        self.operation_db.update_user_info_db(
            {
                self.operation_db.COLUMNS_INFO.time_prediction: set_time
            },
            userid=message.from_user.id
        )

        await message.answer(
            text="Выберите 4 аспекта",
            reply_markup=self.keyboard.get_aspect_selection_ikb
        )

        await state.set_state(states.predictions_1_aspect)
        await state.update_data(set_time=True)
        await state.update_data(period="day")

    def create_router(self):
        self.router.message.register(
            self.set_prediction,
            StateFilter(states.set_time_prediction)
        )

