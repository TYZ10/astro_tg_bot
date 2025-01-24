from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from . import AllTypesGeneration
from example_bot.Tbot import BasicBotOperation
from .get_info_gpt import main_get_info_gpt
from ...Config_bot import states
from ...misc import create_aspects


class Predictions(BasicBotOperation):
    text = """Ты профессиональный астролог. На основе данных о дате, времени и месте рождения составь подробный прогноз {}, учитывая два аспекта, выбранные пользователем. Используй следующую структуру: 1) Введение — цель анализа и его значимость для планирования ближайшего дня. 2) Общая энергетика дня — ключевые тенденции и их влияние на общее состояние. 3) {} — максимально расширенный анализ первых двух выбранных аспектов, их влияние на настроение, события и взаимодействия, минимум 2000 знаков. (например, финансы, здоровье, карьера, отношения, эмоциональный баланс). 4) Физическое и эмоциональное состояние — прогноз, основанный на выбранных аспектах и общем контексте дня. 5) Важные моменты дня — периоды повышенной активности или чувствительности. 6) Рекомендации — персональные советы, учитывающие выбранные аспекты, для достижения гармонии и продуктивности. 7) Заключение — ключевые выводы и основные акценты на день. 8) Совет дня. Не используй термины астрологии, такие как знаки зодиака, названия планет или аспектов, но сохраняй суть их взаимодействия и влияния на выбранные аспекты и жизненные сферы."""

    async def selection_predictions(
            self,
            call: types.CallbackQuery,
            state: FSMContext
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

        await state.update_data(period=period)

        await call.message.answer(
            text="Выберите 2 аспекта из вариантов предоставленных ниже",
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

        if one_aspect == call.data:
            await call.answer(f"Вам нужно выбрать второй аспект отличный от "
                              f"{one_aspect}")
            return

        await call.message.answer("Ожидайте...")

        col_info = self.operation_db.COLUMNS_INFO

        (place_birth, latitude, longitude, time_birth,
         data_birth) = self.operation_db.select_user_info_db(
            f"({col_info.place_birth},"
            f"{col_info.latitude},"
            f"{col_info.longitude},"
            f"{col_info.time_birth},"
            f"{col_info.data_birth})",
            call.from_user.id,
            many=True
        )

        aspects = create_aspects(
            data_birth,
            latitude,
            longitude
        )

        if period == "day":
            text = self.text.format("на день", f"{one_aspect} {call.data}")
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
            f"({self.operation_db.COLUMNS_INFO.generation_count}, "
            f"{self.operation_db.COLUMNS_INFO.generation_count_all})",
            call.from_user.id
        )

        self.operation_db.update_user_info_db(
            {
                self.operation_db.COLUMNS_INFO.generation_count: count_generation - 1,
                self.operation_db.COLUMNS_INFO.generation_count_all: generation_count_all + 1,
            },
            call.from_user.id
        )

        await call.message.answer(
            text=text_gpt
        )

        await call.message.answer(
            text=f"Количество оставшихся генераций: {count_generation - 1}",
            reply_markup=self.keyboard.main_menu_kb
        )

        await state.clear()

    async def create_router(self):
        self.router.callback_query(
            self.selection_predictions,
            F.data == "start generation",
            StateFilter(AllTypesGeneration.predictions.state)
        )
        self.router.callback_query(
            self.get_predictions,
            F.data.split("_")[0] == "select prediction",
            StateFilter(AllTypesGeneration.predictions.state)
        )
        self.router.callback_query(
            self.predictions_1_aspect,
            StateFilter(states.predictions_1_aspect)
        )
        self.router.callback_query(
            self.predictions_2_aspect,
            StateFilter(states.predictions_2_aspect)
        )
