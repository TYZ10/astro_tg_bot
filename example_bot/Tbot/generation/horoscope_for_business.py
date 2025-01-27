from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from . import AllTypesGeneration
from example_bot.Tbot import BasicBotOperation
from .get_info_gpt import main_get_info_gpt, create_aspects


class HoroscopeForBusiness(BasicBotOperation):

    text = "Ты профессиональный астролог, Создай бизнес-прогноз по структуре: 1) Введение — цель и значимость анализа, 2) Личностный бизнес-профиль — лидерство, адаптация, мотивация, 3) Карта талантов — финансы, креативность, организация, 4) Зоны роста — риски, вызовы, эмоциональные триггеры, 5) Профессиональная стратегия — направления, подходы, риски, 6) Периоды успеха — запуск проектов, рост, кризисы, 7) Финансы — стиль управления, инвестиции, расходы, 8) Командная динамика — лидерство, взаимодействие, команда, 9) Долгосрочное видение — влияние, миссия, наследие, 10) Заключение — итоги, вдохновение, советы. Сделай прогноз глубоким, практичным и вдохновляющим. ресные наблюдения. #Примечание: Вывод сделай структурированным, но объёмным. Не используй термины астрологии, такие как знаки зодиака, названия планет, аспектов, но сохраняй суть их взаимодействия и влияния на разные сферы жизни."

    async def horoscope_for_business(
            self,
            call: types.CallbackQuery,
            state: FSMContext):

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

        text_gpt = await main_get_info_gpt(
            self.config,
            aspects,
            self.text
        )
        (count_generation,
         generation_count_all) = self.operation_db.select_user_info_db(
            f"({self.operation_db.COLUMNS_INFO.generation_count}, "
            f"{self.operation_db.COLUMNS_INFO.generation_count_all})",
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
            text=text_gpt
        )

        await call.message.answer(
            text=f"Количество оставшихся генераций: {count_generation - 1}",
            reply_markup=self.keyboard.main_menu_kb
        )

        await state.clear()

    async def create_router(self):
        self.router.callback_query(
            self.horoscope_for_business,
            F.data == "start generation",
            StateFilter(AllTypesGeneration.horoscope_for_business.state)
        )
