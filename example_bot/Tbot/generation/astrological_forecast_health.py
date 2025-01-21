from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from . import AllTypesGeneration
from example_bot.Tbot import BasicBotOperation


class AstrologicalForecastHealth(BasicBotOperation):

    async def astrological_forecast_health(
            self,
            call: types.CallbackQuery,
            state: FSMContext
    ):
        pass

    async def create_router(self):
        self.router.callback_query(
            self.astrological_forecast_health,
            F.data == "start generation",
            StateFilter(AllTypesGeneration.astrological_forecast_health.state)
        )
