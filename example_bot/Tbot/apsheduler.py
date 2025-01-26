from math import ceil

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .basic import BasicBotOperation
from example_bot.misc.datetime_function import (get_day_and_hours_from_date as
                                                get_hour_or_day)


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

    async def update_count_generation(self):
        col_info = self.operation_db.COLUMNS_INFO

        all_info = self.operation_db.select_all_user_info_db(
            f"({col_info.userid}, {col_info.payments_end}, "
            f"{col_info.last_action})"
        )

        self.operation_db.update_all_user_info_db(
            {
                col_info.generation_count: 4
            }
        )

        for userid, payments_end, last_action in all_info:
            if payments_end:
                try:
                    hour = get_hour_or_day(payments_end, get_hour=True)
                    if hour != 0:
                        self.operation_db.update_user_info_db(
                            {
                                col_info.generation_count: 10
                            },
                            userid=userid,
                        )

                        if ceil(hour / 24) == 7 or ceil(hour / 24) == 1:
                            await self.config.bot.send_message(
                                text=f"У вас осталось {ceil(hour / 24)} дней "
                                     f"до окончания подписки. ",
                                chat_id=userid
                            )
                except:
                    pass

            past_day = get_hour_or_day(last_action, past=True)

            if past_day == 2 or past_day == 6 or past_day == 30:
                await self.config.bot.send_message(
                    text="Напоминаю о себе.",
                    chat_id=userid
                )

    async def on_startup(self):
        self.scheduler.add_job(self.update_count_generation,
                               'cron', hour=0, minute=0)
        try:
            self.scheduler.start()
        except:
            pass
