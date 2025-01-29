from aiogram.filters.command import Command
from aiogram import types, F
from aiogram.fsm.context import FSMContext

from . import BasicBotOperation
from .filters import CheckSubFilter


class HelpBot(BasicBotOperation):
    async def help_handler(self, message: types.Message):
        await message.answer("""💡 Нужна помощь? Здесь ты найдёшь ответы на самые популярные вопросы и контакты для обратной связи:

1️⃣ Как работает бот?
Бот использует точные астрономические расчёты и искусственный интеллект, чтобы создавать персонализированные прогнозы, разбирать натальные карты и анализировать совместимость.

2️⃣ Что делать, если возникли технические проблемы?
Если что-то не работает, напиши нам:
📩 По техническим вопросам: @fredkk

3️⃣ Как получить подписку?
Подписку можно оформить за 2 приглашённых друзей, которые сделают хотя бы одну генерацию, или за 150 рублей. Подробнее смотри в разделе "Подписка".

4️⃣ Как работает реферальная система?
Получай бонусы, приглашая друзей! Узнай больше в разделе "Реферальная система".

5️⃣ Вопросы по астрологии?
Если хочешь разобраться в прогнозах или натальной карте глубже, пиши:
📩 По астрологическим вопросам: @Vikki_brilliant

Не нашёл ответа на свой вопрос? Напиши нам, и мы обязательно поможем! 🌟""",
                             reply_markup=self.keyboard.main_menu_kb)

    def create_router(self):
        self.router.message.register(self.help_handler, Command('help'))
        self.router.message.register(self.help_handler, F.text == "Помощь")
