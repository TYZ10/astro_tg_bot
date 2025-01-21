from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from . import AllTypesGeneration
from example_bot.Tbot import BasicBotOperation


class HoroscopeForBusiness(BasicBotOperation):

    async def horoscope_for_business(
            self,
            call: types.CallbackQuery,
            state: FSMContext):
        pass

    async def create_router(self):
        self.router.callback_query(
            self.horoscope_for_business,
            F.data == "start generation",
            StateFilter(AllTypesGeneration.horoscope_for_business.state)
        )
