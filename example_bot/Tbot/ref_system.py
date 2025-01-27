import logging

from aiogram import types, F

from . import BasicBotOperation


class RefSystemBot(BasicBotOperation):
    async def my_ref_handler(self, message: types.Message):

        col_info = self.operation_db.COLUMNS_INFO

        try:
            count_user, count_point = self.operation_db.select_user_info_db(
                f"{col_info.referral_all_count_user}, "
                f"{col_info.referral_all_count_points_user}",
                message.from_user.id,
                many=True
            )
            await message.answer(
                text=f"Ваша реферальная ссылка:\n\n"
                     f"<code>{self.config.URL_BOT}?start={message.from_user.id}</code>\n\n"
                     f"Ваша статистика:\n"
                     f"Количество зарегистрированных рефералов: {count_user}\n"
                     f"Количество рефералов, которые выполнили генерации. "
                     f"{count_point}",
                parse_mode="HTML",
                reply_markup=self.keyboard.main_menu_kb
            )
        except Exception as e:
            logging.error(e, exc_info=True)



    def create_router(self):
        self.router.message.register(self.my_ref_handler,
                            F.text == "Реферальная система")
