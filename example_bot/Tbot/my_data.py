from aiogram.filters.command import Command
from aiogram import types, F
from aiogram.fsm.context import FSMContext

from . import BasicBotOperation


class MyDataBot(BasicBotOperation):
    async def my_data_handler(self, message: types.Message):
        col_info = self.operation_db.COLUMNS_INFO

        data_birth, time_birth, place_birth = self.operation_db.select_user_info_db(
            f"{col_info.data_birth}, {col_info.time_birth}, "
            f"{col_info.place_birth}",
            message.from_user.id,
            many=True
        )

        if not (data_birth and time_birth and place_birth):
            data_birth = "Отсутствует"
            time_birth = "Отсутствует"
            place_birth = "Отсутствует"

        await message.answer(
            text=f"Пользователь: {message.from_user.full_name}\n"
                 f"ID: <code>{message.from_user.id}</code>\n\n"
                 f"Дата рождения: {data_birth}\n"
                 f"Время рождения: {time_birth}\n"
                 f"Место рождения: {place_birth}\n",
            reply_markup=self.keyboard.main_menu_kb
        )

    async def modify_my_data(self, call: types.CallbackQuery):
        pass

    async def create_router(self):
        self.router.message(F.text == "Мои данные", self.my_data_handler)
