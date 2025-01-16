from aiogram.filters.command import Command
from aiogram import types, F

from . import BasicBotOperation


class MainMenuBot(BasicBotOperation):
    async def main_menu(self, message: types.Message):
        """Главное меню"""
        pass

    async def main_menu_call(self, call: types.CallbackQuery):
        """Главное меню через инлайн кнопку"""
        await self.main_menu(call.message)

    def create_router(self):
        self.router.callback_query(F.data == 'main_menu',
                                   self.main_menu_call)
