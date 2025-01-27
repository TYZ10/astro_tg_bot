from aiogram import types, F

from . import BasicBotOperation


class RefSystemBot(BasicBotOperation):
    async def my_ref_handler(self, message: types.Message):

        col_info = self.operation_db.COLUMNS_INFO

        count_user, count_point = self.operation_db.select_user_info_db(
            f"{col_info.referral_all_count_user}, "
            f"{col_info.referral_all_count_points_user}",
            message.from_user.id
        )

        await message.answer(
            text=f"Ваша реферальная ссылка:\n\n"
                 f"<code>{message.bot}?start={message.from_user.id}</code>\n\n"
                 f"Ваша статистика:\n"
                 f"Количество зарегистрированных рефералов: {count_user}\n"
                 f"Количество рефералов, которые выполнили генерации. "
                 f"{count_point}",
            reply_markup=self.keyboard.main_menu_kb,
            parse_mode="HTML"
        )

    async def create_router(self):
        self.router.message(F.text == "Реферальная система",
                            self.my_ref_handler)
