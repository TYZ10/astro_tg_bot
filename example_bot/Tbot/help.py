from aiogram.filters.command import Command
from aiogram import types, F
from aiogram.fsm.context import FSMContext

from . import BasicBotOperation
from .filters import CheckSubFilter


class HelpBot(BasicBotOperation):
    async def help_handler(self, message: types.Message):
        await message.answer("Информация для помощи пользователям.",
                             reply_markup=self.keyboard.main_menu_kb)

    async def create_router(self):
        self.router.message(Command('help'), self.help_handler)
        self.router.message(F.text == "Помощь", self.help_handler)
