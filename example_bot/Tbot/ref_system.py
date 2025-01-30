import logging

from aiogram import types, F

from . import BasicBotOperation


class RefSystemBot(BasicBotOperation):
    async def my_ref_handler(self, call: types.CallbackQuery):
        try:
            col_info = self.operation_db.COLUMNS_INFO

            count_user, count_point = self.operation_db.select_user_info_db(
                f"{col_info.referral_all_count_user}, "
                f"{col_info.referral_all_count_points_user}",
                call.from_user.id,
                many=True
            )
            await call.message.answer(
                text=f"""✨ Хочешь получить подписку бесплатно? У нас есть простая и удобная реферальная система, которая поможет тебе это сделать.

Как это работает:
1️⃣ Получи свою уникальную реферальную ссылку в меню.
2️⃣ Отправь её друзьям и расскажи о возможностях бота: персональные прогнозы, натальная карта, анализ совместимости и многое другое.
3️⃣ Как только 2 твоих друга перейдут по ссылке, начнут пользоваться ботом и сделают хотя бы одну генерацию, твоя подписка активируется автоматически!

Что даёт подписка?

🗓️ Ежедневные гороскопы на выбранные тобой сферы жизни.
🔄 Увеличенное количество генераций — до 8 в день вместо 4.
Чем больше друзей ты пригласишь, тем больше бонусов получишь! Делись своей ссылкой, наслаждайся звёздными подсказками и используй возможности бота на максимум. 🌟

Ваша статистика:
Количество зарегистрированных рефералов: {count_user}
Количество рефералов, которые выполнили генерации: {count_point}

<code>{self.config.URL_BOT}?start={call.from_user.id}</code>""",
                parse_mode="HTML",
                reply_markup=self.keyboard.main_menu_kb
            )
        except Exception as e:
            logging.error(e, exc_info=True)

    def create_router(self):
        self.router.callback_query.register(self.my_ref_handler,
                                    F.data == "🎁 Реферальная система")
