from aiogram.filters.command import Command
from aiogram import types, F
from aiogram.fsm.context import FSMContext

from . import BasicBotOperation


class MyDataBot(BasicBotOperation):
    async def my_data_handler(self, message: types.Message):
        pass

    async def create_router(self):
        self.router.message(F.text == "Мои данные", self.my_data_handler)
