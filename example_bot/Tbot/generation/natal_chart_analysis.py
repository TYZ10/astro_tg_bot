from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from . import AllTypesGeneration
from example_bot.Tbot import BasicBotOperation, states
from .get_info_gpt import main_get_info_gpt
from ...misc import create_aspects


class NatalChartAnalysis(BasicBotOperation):

    text = "#Роль: Профессиональный астролог. #Задание: На основе следующих данных, сделай подробный анализ личности и жизненного пути.  Также проанализируй аспекты между элементами, объясни их влияние, добавь рекомендации, примеры из реальной жизни и интересные наблюдения. #Примечание: Вывод сделай структурированным, но объёмным. Не используй термины астрологии, такие как знаки зодиака, названия планет, аспектов, но сохраняй суть их взаимодействия и влияния на разные сферы жизни. Укажи ключевые аспекты: "

    async def natal_chart_analysis(self, call: types.CallbackQuery,
                                   state: FSMContext):
        await call.message.answer(
            text="Выберите 2 аспекта из вариантов предоставленных ниже",
            reply_markup=self.keyboard.get_aspect_selection_ikb
        )
        await state.set_state(states.natal_chart_analysis_1_aspect)

    async def natal_chart_analysis_1_aspect(self, call: types.CallbackQuery,
                                            state: FSMContext):
        await state.update_data(
            one_aspect=call.data
        )
        await call.answer("Выберите ещё один аспект")

        await state.set_state(states.natal_chart_analysis_2_aspect)

    async def natal_chart_analysis_2_aspect(self, call: types.CallbackQuery,
                                            state: FSMContext):
        st = await state.get_data()

        one_aspect = st['one_aspect']

        if one_aspect == call.data:
            await call.answer(f"Вам нужно выбрать второй аспект отличный от "
                              f"{one_aspect}")
            return

        await call.message.answer("Ожидайте...")

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

        aspects = create_aspects(
            f"{data_birth} {time_birth}",
            latitude,
            longitude
        )

        text_gpt = await main_get_info_gpt(
            self.config,
            f"{one_aspect} {call.data}\n\n {aspects}",
            self.text
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

        await call.message.answer(
            text=str(text_gpt)
        )

        await call.message.answer(
            text=f"Количество оставшихся генераций: {count_generation - 1}",
            reply_markup=self.keyboard.main_menu_kb
        )

        await state.clear()

    def create_router(self):
        self.router.callback_query.register(
            self.natal_chart_analysis,
            F.data == "start generation",
            StateFilter(AllTypesGeneration.natal_chart_analysis.state)
        )
        self.router.callback_query.register(
            self.natal_chart_analysis_1_aspect,
            StateFilter(states.natal_chart_analysis_1_aspect)
        )
        self.router.callback_query.register(
            self.natal_chart_analysis_2_aspect,
            StateFilter(states.natal_chart_analysis_2_aspect)
        )
