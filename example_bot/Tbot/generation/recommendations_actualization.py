from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from . import AllTypesGeneration
from example_bot.Tbot import BasicBotOperation


class RecommendationsActualization(BasicBotOperation):

    async def recommendations_actualization(
            self,
            call: types.CallbackQuery,
            state: FSMContext
    ):
        pass

    async def create_router(self):
        self.router.callback_query(
            self.recommendations_actualization,
            F.data == "start generation",
            StateFilter(
                AllTypesGeneration.recommendations_self_actualization.state
            )
        )
