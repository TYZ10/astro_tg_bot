from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from . import AllTypesGeneration
from example_bot.Tbot import BasicBotOperation


class AnalyzingCompatibilityRelationship(BasicBotOperation):

    async def analyzing_compatibility_relationship(
            self,
            place_birth,
            latitude,
            longitude,
            time_birth,
            data_birth,
    ):
        """Анализ совместимости в отношениях"""

    async def create_router(self):
        pass
