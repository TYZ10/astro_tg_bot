import asyncio

from aiogram.filters.command import Command
from aiogram import types
from aiogram.fsm.context import FSMContext

from . import BasicBotOperation
from .filters import CheckSubFilter


class StartBot(BasicBotOperation):
    async def start(self, message: types.Message, state: FSMContext):
        """Стартовый хэндлер"""

        is_new_user = self.operation_db.insert_new_user(
            message.from_user.id,
            message.from_user.full_name,
            message.from_user.username
        )

        await message.answer(
            text=f"Привет {message.from_user.first_name}, я бот с "
                 f"астрономическими функциями.",
            reply_markup=self.keyboard.main_menu_kb
        )

        await asyncio.sleep(1)

        if is_new_user:
            await self.subscribe(message, state)

            ref_userid = message.text.split(' ', 1)[-1]
            if ref_userid != '/start':
                ref_userid = int(ref_userid)

                col_info = self.operation_db.COLUMNS_INFO

                referral_all_count_user = \
                    self.operation_db.select_user_info_db(
                        col_info.referral_all_count_user,
                        message.from_user.id
                    )

                self.operation_db.update_user_info_db(
                    {
                        col_info.referral_user: ref_userid,
                        col_info.referral_all_count_user:
                            referral_all_count_user + 1
                    },
                    message.from_user.id
                )

    async def subscribe(self, message_or_call, state: FSMContext):
        """Хэндлер для подписки на канал"""

        await state.clear()

        if isinstance(message_or_call, types.CallbackQuery):
            message_or_call = message_or_call.message

        await message_or_call.answer(
            text="Вы не подписались на наш канал, подпишитесь что бы "
                 "пользоваться ботом.",
            reply_markup=self.keyboard.subscribe_ikb
        )
        await message_or_call.answer(
            text="Перемещаю в главное меню.",
            reply_markup=self.keyboard.main_menu_kb
        )

    def create_router(self):
        self.router.message.register(self.start, Command("start"))
        self.router.message.register(self.subscribe,
                                     CheckSubFilter(self.config,
                                                    self.operation_db))
        self.router.callback_query.register(self.subscribe,
                                            CheckSubFilter(self.config,
                                                           self.operation_db))
