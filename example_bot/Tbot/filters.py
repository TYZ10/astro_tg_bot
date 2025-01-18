from aiogram.filters import BaseFilter

from .check_sub import check_sub
from . import ConfigBot


class CheckSubFilter(BaseFilter):
    """Проверяет на подписку"""
    def __init__(self, config: ConfigBot):
        self.config = config

    async def __call__(self, message_or_call) -> bool:
        userid = message_or_call.from_user.id
        return not (await check_sub(message_or_call.bot, self.config, userid))
