from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from . import AllTypesGeneration
from example_bot.Tbot import BasicBotOperation
from .get_info_gpt import main_get_info_gpt
from example_bot.Config_bot import states
from example_bot.misc import create_aspects
from example_bot.misc.datetime_function import get_day_and_hours_from_date


class Predictions(BasicBotOperation):
    text = """Ты профессиональный астролог. На основе данных о дате, времени и месте рождения составь подробный прогноз {}, учитывая два аспекта, выбранные пользователем. Используй следующую структуру: 1) Введение — цель анализа и его значимость для планирования ближайшего дня. 2) Общая энергетика дня — ключевые тенденции и их влияние на общее состояние. 3) {} — максимально расширенный анализ первых двух выбранных аспектов, их влияние на настроение, события и взаимодействия, минимум 2000 знаков. (например, финансы, здоровье, карьера, отношения, эмоциональный баланс). 4) Физическое и эмоциональное состояние — прогноз, основанный на выбранных аспектах и общем контексте дня. 5) Важные моменты дня — периоды повышенной активности или чувствительности. 6) Рекомендации — персональные советы, учитывающие выбранные аспекты, для достижения гармонии и продуктивности. 7) Заключение — ключевые выводы и основные акценты на день. 8) Совет дня. Не используй термины астрологии, такие как знаки зодиака, названия планет или аспектов, но сохраняй суть их взаимодействия и влияния на выбранные аспекты и жизненные сферы."""

    async def main_start_predictions(
            self,
            message: types.Message,
            state: FSMContext,
    ):
        await state.set_state(AllTypesGeneration()[message.text])
        await message.answer(
            text="""Звёзды готовы раскрыть тебе тайны будущего! ✨ Наш бот создаёт персональные прогнозы, чтобы ты мог осознанно планировать важные события, использовать благоприятные периоды и обходить возможные сложности. Выбери свой прогноз:

📆 Прогноз на следующий месяц — детальный анализ ближайших 30 дней: ключевые события, возможности, вызовы и периоды максимальной активности.

💼 Бизнес-гороскоп — когда лучше принимать важные решения, запускать проекты, управлять финансами и искать новые возможности.

❤️‍🩹 Астрологический прогноз для здоровья — на что обратить внимание, когда беречь себя, а когда наоборот — заряжаться энергией и действовать на полную мощность.

☀️ Ежедневные прогнозы — получай персональные предсказания на каждый день, чтобы жить в ритме со Вселенной (доступно по подписке).

💞 Анализ совместимости в отношениях — разбор глубины вашей связи, понимание сильных и сложных сторон пары, советы для гармонии и роста.

Будущее уже написано в звёздах, а теперь оно станет понятным и доступным для тебя! 🔥🌌""",
            reply_markup=self.keyboard.predictions_and_horoscopes_ikb
        )

    async def daily_forecasts(
            self,
            message: types.Message
    ):
        await message.answer(
            text="""☀️ Хочешь начинать каждый день с подсказок от звёзд? Ежедневный гороскоп составляется специально для тебя и приходит вечером в удобное время, которое ты выбираешь. Ты можешь выбрать до 4 сфер, которые для тебя наиболее важны:
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

Звёзды готовы раскрыть свои тайны! Жми кнопку и начни получать свои прогнозы каждый день. 🚀""",
            reply_markup=self.keyboard.daily_forecasts_ikb
        )

    async def selection_predictions(
            self,
            call: types.CallbackQuery
    ):
        await call.message.answer(
            text="Выберите период предсказания:",
            reply_markup=self.keyboard.selection_predictions_ikb
        )

    async def get_predictions(
            self,
            call: types.CallbackQuery,
            state: FSMContext):
        _, period = call.data.split("_", maxsplit=1)

        if period == "day":
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

            col_info = self.operation_db.COLUMNS_INFO

            payments_end = self.operation_db.select_user_info_db(
                col_info.payments_end,
                call.from_user.id
            )

            if get_day_and_hours_from_date(payments_end) <= 0:
                await call.message.answer(
                    text="""Ежедневный гороскоп доступен по подписке. Ты можешь её оформить:
✨ За 2 приглашённых друзей, которые сделают хотя бы одну генерацию.
✨ Или за символическую плату всего 150 рублей — это поможет поддерживать работу бота и оплачивать необходимые сервисы.
""",
                    reply_markup=self.keyboard.payments_ikb
                )
                return
        elif period == "month":
             text = """📅 Гороскоп на месяц — это краткий и точный прогноз на 30 дней. Ты узнаешь, где тебя ждёт успех, а где стоит быть внимательнее. Звёзды подскажут лучшие моменты для действий. 🌙"

Пояснение про выбор аспектов:
"Перед составлением прогноза выбери 2 аспекта, которые сейчас особенно важны:

💼 Финансы и карьера
❤️ Любовь и отношения
🏠 Семья и домашние дела
🌟 Духовный рост и саморазвитие
🏥 Здоровье и энергия
⚠️ Опасности и предупреждения
✨ Миссия и предназначение
Каждый месяц уникален, и этот прогноз поможет тебе использовать его возможности на максимум. Жми кнопку и узнавай, что тебя ждёт! 🌠"""
        else:
            text = """🗓️ Гороскоп на год — это твой личный путеводитель на целый год. Ты узнаешь, какие возможности и вызовы ждут тебя, в какие моменты стоит действовать, а когда лучше сделать паузу. Всё это — на основе твоих астрологических данных! 🌟"


Пояснение про выбор аспектов:
"Перед составлением прогноза выбери 2 аспекта, которые для тебя наиболее важны:

💼 Финансы и карьера
❤️ Любовь и отношения
🏠 Семья и домашние дела
🌟 Духовный рост и саморазвитие
🏥 Здоровье и энергия
⚠️ Опасности и предупреждения
✨ Миссия и предназначение
Твой прогноз поможет планировать важные события и оставаться в гармонии с энергиями года. Жми кнопку и готовься к 2025 году! 🚀
"""

        await state.update_data(period=period)

        await call.message.answer(
            text=text,
            reply_markup=self.keyboard.get_aspect_selection_ikb
        )
        await state.set_state(states.predictions_1_aspect)

    async def predictions_1_aspect(
            self,
            call: types.CallbackQuery,
            state: FSMContext
    ):
        await state.update_data(
            one_aspect=call.data
        )
        await call.answer("Выберите ещё один аспект")

        await state.set_state(states.predictions_2_aspect)

    async def predictions_2_aspect(
            self,
            call: types.CallbackQuery,
            state: FSMContext
    ):

        st = await state.get_data()
        period = st["period"]

        one_aspect = st['one_aspect']
        two_aspects = st.get("two_aspect")
        three_aspects = st.get("three_aspect")

        if (one_aspect == call.data or two_aspects == call.data or
                three_aspects == call.data):
            await call.answer(f"Вам нужно выбрать неодинаковые аспекты!!")
            return

        if period == "day":
            if two_aspects:
                if three_aspects:
                    all_aspects = (f"{one_aspect}, {two_aspects}, ",
                                   f"{three_aspects}, {call.data}")
                else:
                    await state.update_data(
                        three_aspect=call.data
                    )
                    await call.answer("Выберите ещё один аспект")
                    return
            else:
                await state.update_data(
                    two_aspect=call.data
                )
                await call.answer("Выберите ещё один аспект")
                return

        col_info = self.operation_db.COLUMNS_INFO

        (place_birth, latitude, longitude, time_birth,
         data_birth) = self.operation_db.select_user_info_db(
            f"{col_info.place_birth}, "
            f"{col_info.latitude}, "
            f"{col_info.longitude}, "
            f"{col_info.time_birth}, "
            f"{col_info.data_birth}",
            call.from_user.id,
            many=True
        )

        if place_birth is None or time_birth is None or data_birth is None:
            text = "Перед началом генерации нужно ввести ваши данные."
            keyboard = self.keyboard.no_generation_data_ikb
            await call.message.edit_text(text=text, reply_markup=keyboard)
            await state.clear()
            return

        await call.message.answer("Ожидайте, примерное время 25-35 секунд ")

        aspects = create_aspects(
            f"{data_birth} {time_birth}",
            latitude,
            longitude
        )

        if period == "day":
            text = self.text.format("на день", all_aspects)
        elif period == "month":
            text = self.text.format("на месяц", f"{one_aspect} {call.data}")
        else:
            text = self.text.format("на год", f"{one_aspect} {call.data}")

        text_gpt = await main_get_info_gpt(
            self.config,
            f"{aspects}",
            text
        )
        (count_generation,
         generation_count_all) = self.operation_db.select_user_info_db(
            f"{self.operation_db.COLUMNS_INFO.generation_count}, "
            f"{self.operation_db.COLUMNS_INFO.generation_count_all}",
            call.from_user.id,
            many=True
        )

        self.operation_db.update_user_info_db(
            {
                self.operation_db.COLUMNS_INFO.generation_count: count_generation - 1,
                self.operation_db.COLUMNS_INFO.generation_count_all: generation_count_all + 1,
            },
            call.from_user.id
        )

        if len(str(text_gpt)) > 4096:
            await call.message.answer(str(text_gpt)[:4096])
            await call.message.answer(str(text_gpt)[4096:])
        else:
            await call.message.answer(
                text=str(text_gpt)
            )

        await call.message.answer(
            text=f"Количество оставшихся генераций: {count_generation - 1}",
            reply_markup=self.keyboard.main_menu_kb
        )

        await state.clear()

    def create_router(self):
        self.router.message.register(
            self.main_start_predictions,
            F.text == "🌟 Прогнозы и гороскопы"
        )
        self.router.message.register(
            self.daily_forecasts,
            F.text == "☀️ Ежедневные прогнозы"
        )
        self.router.callback_query.register(
            self.selection_predictions,
            F.data == "start generation",
            StateFilter(AllTypesGeneration.predictions.state)
        )
        self.router.callback_query.register(
            self.get_predictions,
            F.data.split("_")[0] == "select prediction",
            StateFilter(AllTypesGeneration.predictions.state)
        )
        self.router.callback_query.register(
            self.predictions_1_aspect,
            StateFilter(states.predictions_1_aspect)
        )
        self.router.callback_query.register(
            self.predictions_2_aspect,
            StateFilter(states.predictions_2_aspect)
        )
