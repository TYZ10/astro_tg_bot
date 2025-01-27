from .Config_bot import ConfigBot
from .Tbot import KeyboardBot
from .Tbot.handler import InitHandlerBot
from .operation_db import OperationDataBaseBot


class TelegramBot:
    def __init__(self):
        self.config: ConfigBot = ConfigBot()
        self.operation_db: OperationDataBaseBot = OperationDataBaseBot(
            self.config.POSTGRESQL_TABLE_NAME,
            self.config.POSTGRESQL_USER,
            self.config.POSTGRESQL_PASSWORD,
            self.config.POSTGRESQL_DBNAME,
            is_delete_db=True # УДАЛЯЕТ АБСОЛЮТНО ВСЮ ИНФОРМАЦИЮ БЕЗВОЗВРАТНО!!!!!
        )
        self.keyboard: KeyboardBot = KeyboardBot(self.config)

    async def __create_bot(self):
        await self.config.skip_updates()
        InitHandlerBot(
            self.config,
            self.operation_db,
            self.keyboard,
        )

    async def start_bot(self):
        await self.__create_bot()

        try:
            await self.config.dp.start_polling(self.config.bot)
        except Exception as e:
            print(e)



