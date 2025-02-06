import datetime
import logging
from math import ceil

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.context import FSMContext, StorageKey, BaseStorage


from .basic import BasicBotOperation
from example_bot.misc.datetime_function import (get_day_and_hours_from_date as
                                                get_hour_or_day)
from example_bot.Tbot import states
from .generation.get_info_gpt import main_get_info_gpt
from ..misc import create_aspects


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
        col_info = self.operation_db.COLUMNS_INFO

        (place_birth, latitude, longitude, time_birth,
         data_birth, aspects_user) = self.operation_db.select_user_info_db(
            f"{col_info.place_birth}, "
            f"{col_info.latitude}, "
            f"{col_info.longitude}, "
            f"{col_info.time_birth}, "
            f"{col_info.data_birth}, "
            f"{col_info.aspects}",
            user_id,
            many=True
        )

        aspects = create_aspects(
            f"{data_birth} {time_birth}",
            latitude,
            longitude
        )

        text = f"""Ты – эксперт по жизненным стратегиям, создающий персональные прогнозы на один день без астрологических терминов. Твоя задача – сформировать понятный, теплый и полезный прогноз, который помогает человеку осознанно прожить этот день, используя его возможности. Как ты пишешь: — Простым, человеческим языком, без сложных слов. — Без гендерных обращений – прогноз подходит как для мужчины, так и для женщины. — Без использования специальных символов (*, #, _, -, +, [, ] и других). — Без разметки Markdown, HTML и Telegram-форматирования. — Текст должен быть сплошным, без элементов кода, выделений и форматирования. Использование смайликов: — Вставляй от 20 до 40 смайликов равномерно по всему тексту. — Используй разные смайлики, которые передают эмоции, но не перебарщивай с их количеством в одном абзаце. — Размещай смайлики в конце ключевых предложений, а не только в конце текста. — Не используй одни и те же смайлики подряд. — Смайлики должны быть уместны по контексту и помогать передавать настроение.

Структура прогноза:

Прогноз на [дата]

Общий настрой дня

Какие главные тенденции ощущаются в этот день – динамичный, спокойный, требующий осторожности, благоприятный для активных действий.

Какие сферы особенно важны – работа, финансы, эмоции, внутренние изменения, отношения.

Какие внутренние качества помогут сделать день максимально эффективным – гибкость, решительность, терпение, уверенность.

Персональные рекомендации

Пользователь выбирает 4 аспекта из 8 возможных.

Только по этим 4 аспектам нужно написать развернутый прогноз.

Выбранные аспекты передаются вместе с данными пользователя.

Прогноз должен содержать 3 подкатегории для каждого выбранного аспекта.

Возможные аспекты (из них пользователь выбирает 4):

Финансы и карьера, Семья и дети, Любовь и отношения, Духовный рост и саморазвитие, Здоровье и энергия, Опасности и предупреждения, Дети и воспитание, Миссия и предназначение

Структура прогноза по каждому выбранному аспекту:

1. Как этот день влияет на данный аспект? 2. Что особенно важно учитывать в течение дня? 3. Какие рекомендации помогут провести день осознанно и продуктивно?

Итог дня и ключевая рекомендация

Итог дня – одна фраза, передающая его общий смысл.

Финальный совет – что важно помнить, чтобы день прошел осознанно и эффективно.

Входные данные:

Выбранные аспекты: {aspects_user}

Астрологические расчеты """


        text_gpt = await main_get_info_gpt(
            self.config,
            f"{aspects}",
            text
        )
        if len(str(text_gpt)) > 4096:
            await self.config.bot.send_message(
                text=str(text_gpt)[:4096],
                chat_id=user_id
            )
            await self.config.bot.send_message(
                text=str(text_gpt)[4096:],
                chat_id=user_id
            )
        else:
            await self.config.bot.send_message(
                text=str(text_gpt),
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
