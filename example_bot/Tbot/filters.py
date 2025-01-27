from datetime import datetime

from aiogram.filters import BaseFilter

from .check_sub import check_sub
from . import ConfigBot, OperationDataBaseBot


class CheckSubFilter(BaseFilter):
    """Проверяет на подписку"""
    def __init__(self, config: ConfigBot, operation_db: OperationDataBaseBot):
        self.config = config
        self.operation_db = operation_db

    async def __call__(self, message_or_call) -> bool:
        userid = message_or_call.from_user.id

        self.operation_db.update_user_info_db(
            {
                self.operation_db.COLUMNS_INFO.last_action:
                    datetime.now(),
            },
            userid
        )

        return not (await check_sub(message_or_call.bot, self.config, userid))
