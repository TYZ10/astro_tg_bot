from aiogram import types, F
from . import AllTypesGeneration as types_gen

from example_bot.Tbot import BasicBotOperation


class StartAllGeneration(BasicBotOperation):
    # Начало любой генерации

    async def start_generation(self,
                               message: types.Message):
        count_generation = self.operation_db.select_user_info_db(
            self.operation_db.COLUMNS_INFO.generation_count,
            message.from_user.id
        )
        if count_generation > 0:
            text = "Хотите ввести новые данные или использовать предыдущие?"
            keyboard = self.keyboard.start_generation_ikb
        else:
            text = ("Вы использовали все доступные генерации. "
                    "Новые генерации будут доступны завтра в 00:00 по МСК.")
            keyboard = self.keyboard.main_menu_kb

        await message.answer(
            text=text,
            reply_markup=keyboard
        )

    async def create_router(self):
        self.router.message(
            self.start_generation,
            F.text == types_gen.recommendations_self_actualization.text
        )
        self.router.message(
            self.start_generation,
            F.text == types_gen.natal_chart_analysis.text
        )
        self.router.message(
            self.start_generation,
            F.text == types_gen.predictions.text
        )
        self.router.message(
            self.start_generation,
            F.text == types_gen.horoscope_for_business.text
        )
        self.router.message(
            self.start_generation,
            F.text == types_gen.analyzing_compatibility_relationship.text
        )
        self.router.message(
            self.start_generation,
            F.text == types_gen.astrological_forecast_health.text
        )