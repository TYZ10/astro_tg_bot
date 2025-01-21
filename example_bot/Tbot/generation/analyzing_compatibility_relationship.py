from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from . import AllTypesGeneration
from example_bot.Tbot import BasicBotOperation


class AnalyzingCompatibilityRelationship(BasicBotOperation):

    async def analyzing_compatibility_relationship(
            self,
            call: types.CallbackQuery,
            state: FSMContext
    ):
        pass

    async def create_router(self):
        self.router.callback_query(
            self.analyzing_compatibility_relationship,
            F.data == "start generation",
            StateFilter(
                AllTypesGeneration.analyzing_compatibility_relationship.state
            )
        )
