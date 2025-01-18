from aiogram import types, F
from aiogram.fsm.context import FSMContext

from . import BasicBotOperation


class MainMenuBot(BasicBotOperation):
    async def main_menu(self, message: types.Message,
                             state: FSMContext):
        """Главное меню"""
        await state.clear()

    async def main_menu_call(self, call: types.CallbackQuery,
                             state: FSMContext):
        """Главное меню через инлайн кнопку"""
        await self.main_menu(call.message, state)

    def create_router(self):
        self.router.callback_query(F.data == 'main_menu',
                                   self.main_menu_call)
