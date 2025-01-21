from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from . import AllTypesGeneration
from example_bot.Tbot import BasicBotOperation


class NatalChartAnalysis(BasicBotOperation):

    async def natal_chart_analysis(self, call: types.CallbackQuery,
                                   state: FSMContext):
        pass

    async def create_router(self):
        self.router.callback_query(
            self.natal_chart_analysis,
            F.data == "start generation",
            StateFilter(AllTypesGeneration.natal_chart_analysis.state)
        )
