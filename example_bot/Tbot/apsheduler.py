import datetime
import logging
from math import ceil

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.context import FSMContext, StorageKey, BaseStorage


from .basic import BasicBotOperation
from example_bot.misc.datetime_function import (get_day_and_hours_from_date as
                                                get_hour_or_day)
from example_bot.Tbot import states


class ApshedulerBot(BasicBotOperation):
    def __init__(self, config, operation_db, keyboard):
        super().__init__(
            config,
            operation_db,
            keyboard
        )
        self.scheduler: AsyncIOScheduler = AsyncIOScheduler(
            timezone='Europe/Moscow'
        )

    async def __start_prediction(
            self,
            user_id: int,
    ):

        text = """☀️ Хочешь начинать каждый день с подсказок от звёзд? Ежедневный гороскоп составляется специально для тебя и приходит вечером в удобное время, которое ты выбираешь. Ты можешь выбрать до 4 сфер, которые для тебя наиболее важны:
💼 Финансы и карьера
👨‍👩‍👧‍👦 Семья и дети
❤️ Любовь и отношения
🌟 Духовный рост и саморазвитие
🏥 Здоровье и энергия
⚠️ Опасности и предупреждения
👶 Дети и воспитание
✨ Миссия и предназначение

Ежедневный гороскоп доступен по подписке. Ты можешь её оформить:
✨ За 2 приглашённых друзей, которые сделают хотя бы одну генерацию.
✨ Или за символическую плату всего 150 рублей — это поможет поддерживать работу бота и оплачивать необходимые сервисы.

Звёзды готовы раскрыть свои тайны! Жми кнопку и начни получать свои прогнозы каждый день. 🚀"""

        state = FSMContext(
            self.config.STOR,
            StorageKey(
                self.config.bot.id,
                user_id,
                user_id
            )
        )

        await state.set_state(states.predictions_1_aspect)

        await state.update_data(period="day")

        await self.config.bot.send_message(
            text=text,
            reply_markup=self.keyboard.get_aspect_selection_ikb,
            chat_id=user_id
        )

    async def update_count_generation(self):

        await self.get_report()

        col_info = self.operation_db.COLUMNS_INFO

        all_info = self.operation_db.select_all_user_info_db(
            f"{col_info.userid}, {col_info.payments_end}, "
            f"{col_info.last_action}"
        )

        self.operation_db.update_all_user_info_db(
            {
                col_info.generation_count: 4
            }
        )

        for userid, payments_end, last_action in all_info:
            if payments_end:
                try:
                    days = get_hour_or_day(payments_end)

                    if days != 0:
                        self.operation_db.update_user_info_db(
                            {
                                col_info.generation_count: 10
                            },
                            userid=userid,
                        )

                        if days == 7 or days == 1:
                            await self.config.bot.send_message(
                                text=f"У вас осталось {days} дней "
                                     f"до окончания подписки. ",
                                chat_id=userid
                            )
                except Exception as e:
                    logging.exception(e)

            past_day = get_hour_or_day(last_action, past=True)

            if past_day == 2 or past_day == 6 or past_day == 30:
                await self.config.bot.send_message(
                    text="""Привет! 🌟

Ты ещё не подписался, а звёзды уже готовы раскрыть для тебя секреты натальной карты, прогнозов и совместимости.

Напоминаю, что бот полностью бесплатный, но доступ возможен только после подписки. Это важно для поддержания его работы и развития.

Жми кнопку ниже, чтобы подписаться и начать своё путешествие по Вселенной. ✨ Не упусти шанс узнать, что говорят звёзды! 🚀""",
                    chat_id=userid
                )

    async def check_time_prediction(self):
        col_info = self.operation_db.COLUMNS_INFO

        time_now = datetime.datetime.now()

        all_info = self.operation_db.select_all_user_info_db(
            f"{col_info.time_prediction}, {col_info.payments_end}, "
            f"{col_info.userid}"
        )
        for time_prediction, payments_end, userid in all_info:
            if get_hour_or_day(payments_end) != 0:
                if time_now.minute == time_prediction.minute:
                    try:
                        await self.__start_prediction(
                            user_id=userid
                        )
                    except:
                        pass

    async def get_report(self):
        result = self.operation_db.select_all_user_info_db(
            f"{self.operation_db.COLUMNS_INFO.first_arrival}, "
            f"{self.operation_db.COLUMNS_INFO.generation_count}, "
            f"{self.operation_db.COLUMNS_INFO.payments_end}, "
            f"{self.operation_db.COLUMNS_INFO.referral_user}"
        )

        count_new_user = 0
        count_generations = 0
        count_referrals_user = 0

        for first_arrival, generation_count, payments_end, \
                referral_user in result:
            if get_hour_or_day(first_arrival) <= 1:
                count_new_user += 1
                if referral_user:
                    count_referrals_user += 1

            try:
                if payments_end and \
                        get_hour_or_day(payments_end, get_hour=True) != 0:
                    count_generations += 10 - generation_count
                else:
                    count_generations += 4 - generation_count
            except:
                count_generations += 4 - generation_count

        for i in self.config.ADMINS_ID:
            try:
                await self.config.bot.send_message(
                    text=(f"Отчёт за сегодня:\n\n"
                          f"Новых пользователей: {count_new_user}\n"
                          f"Генераций: {count_generations}\n"
                          f"Рефералов: {count_referrals_user}\n"),
                    chat_id=i
                )
            except:
                pass

    async def on_startup(self):
        self.scheduler.add_job(self.update_count_generation,
                               'cron', hour=18, minute=3)
        self.scheduler.add_job(
            self.check_time_prediction,
            'interval',
            minutes=1
        )
        try:
            self.scheduler.start()
        except:
            pass

    def create_router(self):
        print("start bot")
