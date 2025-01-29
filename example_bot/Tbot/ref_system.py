import logging

from aiogram import types, F

from . import BasicBotOperation


class RefSystemBot(BasicBotOperation):
    async def my_ref_handler(self, call: types.CallbackQuery):
        try:
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

<code>{self.config.URL_BOT}?start={call.from_user.id}</code>""",
                parse_mode="HTML",
                reply_markup=self.keyboard.main_menu_kb
            )
        except Exception as e:
            logging.error(e, exc_info=True)

    def create_router(self):
        self.router.callback_query.register(self.my_ref_handler,
                                    F.data == "🎁 Реферальная система")
