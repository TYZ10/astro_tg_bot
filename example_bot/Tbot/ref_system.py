from aiogram.filters.command import Command
from aiogram import types, F
from aiogram.fsm.context import FSMContext

from . import BasicBotOperation


class MyDataBot(BasicBotOperation):
    async def my_ref_handler(self, message: types.Message):
        await message.answer(
            text=f"Ваша реферальная ссылка:\n"
                 f"<code>{message.bot}?start={message.from_user.id}</code>\n\n"
                 f"",
            reply_markup=self.keyboard.main_menu_kb,
            parse_mode="HTML"
        )

    async def create_router(self):
        self.router.message(F.text == "Реферальная система", self.my_ref_handler)
