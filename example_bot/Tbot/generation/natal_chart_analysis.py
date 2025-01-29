from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from . import AllTypesGeneration
from example_bot.Tbot import BasicBotOperation, states
from .get_info_gpt import main_get_info_gpt
from ...misc import create_aspects


class NatalChartAnalysis(BasicBotOperation):

    text = "#Роль: Профессиональный астролог. #Задание: На основе следующих данных, сделай подробный анализ личности и жизненного пути.  Также проанализируй аспекты между элементами, объясни их влияние, добавь рекомендации, примеры из реальной жизни и интересные наблюдения. #Примечание: Вывод сделай структурированным, но объёмным. Не используй термины астрологии, такие как знаки зодиака, названия планет, аспектов, но сохраняй суть их взаимодействия и влияния на разные сферы жизни. Укажи ключевые аспекты: "

    async def main_menu_natal_chart_analysis(self, message: types.Message):
        await message.answer(
            text="""Твоя натальная карта — это твой личный звёздный код, который раскрывает таланты, сильные стороны и путь к гармонии. 🌌 Бот поможет расшифровать влияние звёзд на твою жизнь, разобрать скрытые аспекты личности и дать полезные рекомендации. Выбери, что тебе интересно:

🪐 Анализ натальной карты — детальный разбор твоего звёздного кода: личность, судьба, скрытые ресурсы и особенности характера.

✨ Анализ сильных сторон личности — твои таланты, внутренние опоры и ключевые качества, которые помогут достигать целей и раскрыть потенциал.

🚀 Рекомендации по самореализации — как найти своё предназначение, в какой сфере раскрыть себя, какие шаги помогут двигаться к успеху.

Выбирай и раскрывай тайны своей натальной карты! 🔥💫""",
            reply_markup=self.keyboard.natal_card_menu_ikb
        )

    async def natal_chart_analysis(self, call: types.CallbackQuery,
                                   state: FSMContext):
        await call.message.answer(
            text="""✨ Анализ натальной карты — это уникальный разбор твоего астрологического кода, созданного на основе твоей даты, времени и места рождения. Карта расскажет о твоих сильных сторонах, скрытых талантах, жизненных задачах и поможет глубже понять себя. 🌌"

Пояснение про выбор аспектов:

"Перед началом анализа выбери 2 аспекта, которые для тебя наиболее важны. Вот варианты:

💼 Финансы и карьера
👨‍👩‍👧‍👦 Семья и дети
❤️ Любовь и отношения
🌟 Духовный рост и саморазвитие
🏥 Здоровье и энергия
⚠️ Опасности и предупреждения
👶 Дети и воспитание
✨ Миссия и предназначение
Анализ будет специально адаптирован под твои приоритеты. Жми кнопку ниже, чтобы узнать больше о себе и своём пути! 🌠""",
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
        self.router.message.register(
            self.main_menu_natal_chart_analysis,
            F.text == "🔮 Анализ натальной карты"
        )
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
