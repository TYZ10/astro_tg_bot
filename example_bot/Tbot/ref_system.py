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
                text=f"""✨ Хочешь получить подписку бесплатно? У нас есть простая и удобная реферальная система, которая поможет тебе это сделать.

Как это работает:
1️⃣ Получи свою уникальную реферальную ссылку в меню.
2️⃣ Отправь её друзьям и расскажи о возможностях бота: персональные прогнозы, натальная карта, анализ совместимости и многое другое.
3️⃣ Как только 2 твоих друга перейдут по ссылке, начнут пользоваться ботом и сделают хотя бы одну генерацию, твоя подписка активируется автоматически!

Что даёт подписка?

🗓️ Ежедневные гороскопы на выбранные тобой сферы жизни.
🔄 Увеличенное количество генераций — до 8 в день вместо 4.
Чем больше друзей ты пригласишь, тем больше бонусов получишь! Делись своей ссылкой, наслаждайся звёздными подсказками и используй возможности бота на максимум. 🌟

<code>{self.config.URL_BOT}?start={message.from_user.id}</code>""",
                parse_mode="HTML",
                reply_markup=self.keyboard.main_menu_kb
            )
        except Exception as e:
            logging.error(e, exc_info=True)



    def create_router(self):
        self.router.message.register(self.my_ref_handler,
                            F.text == "Реферальная система")
