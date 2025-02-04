from aiogram import types, F
from aiogram.fsm.context import FSMContext

from . import BasicBotOperation


class MainMenuBot(BasicBotOperation):
    async def main_menu(self, message: types.Message,
                             state: FSMContext):
        """Главное меню"""
        await state.clear()
        await message.answer(
            text="Главное меню",
            reply_markup=self.keyboard.main_menu_kb,
        )

    async def main_menu_call(self, call: types.CallbackQuery,
                             state: FSMContext):
        """Главное меню через инлайн кнопку"""
        await call.message.delete()
        await self.main_menu(call.message, state)

    def create_router(self):
        self.router.callback_query.register(self.main_menu_call,
                                   F.data == 'main menu')
