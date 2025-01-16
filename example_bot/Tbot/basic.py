from abc import ABC, abstractmethod

from aiogram import types, Router

from . import (
    OperationDataBaseBot, ConfigBot
)


class BasicBotOperation(ABC):
    """Базовая конструкция для почти всех модулей бота"""

    from . import KeyboardBot

    def __init__(self,
                 config: ConfigBot,
                 operation_db: OperationDataBaseBot,
                 keyboard: KeyboardBot):
        from . import KeyboardBot

        self.config: ConfigBot = config
        self.operation_db: OperationDataBaseBot = operation_db
        self.keyboard: KeyboardBot = keyboard
        self.router: Router = Router()

        self.create_router()

    @abstractmethod
    async def create_router(self):
        """Создание роутера"""

