import logging

from aiogram import types, F
from aiogram.fsm.context import FSMContext
from yookassa import Payment, Configuration
from example_bot.misc.datetime_function import get_day_and_hours_from_date

from . import BasicBotOperation, states
from example_bot.misc.datetime_function import create_new_payments_end


class PaymentsBot(BasicBotOperation):

    async def __check_and_update_info_payments(
            self,
            payments_id,
            message_or_call: types.Message or types.CallbackQuery
    ):
        col_info = self.operation_db.COLUMNS_INFO

        if payments_id:
            if self.check_user_payments(payments_id):
                payments_end = self.operation_db.select_user_info_db(
                    col_info.payments_end,
                    message_or_call.from_user.id
                )
                new_pay_end_date = create_new_payments_end(payments_end)

                self.operation_db.update_user_info_db(
                    {
                        col_info.payments_id: None,
                        col_info.payments_end: new_pay_end_date
                    },
                    message_or_call.from_user.id
                )

                if isinstance(message_or_call, types.Message):
                    await message_or_call.answer(
                        text="Я заметил не проверенную вами оплату подписки, "
                             "продлеваю вашу подписку.",
                        reply_markup=self.keyboard.main_menu_kb,
                    )
                else:
                    await message_or_call.message.answer(
                        text="Я заметил не проверенную вами оплату подписки, "
                             "продлеваю вашу подписку.",
                        reply_markup=self.keyboard.main_menu_kb,
                    )

                return True
            else:
                self.operation_db.update_user_info_db(
                    {
                        col_info.payments_id: None
                    },
                    message_or_call.from_user.id
                )

    def __create_payments(self, full_name: str):
        """Создание оплаты"""

        #  https://yookassa.ru/developers/api#payment_object
        #  https://yookassa.ru/developers/api#create_payment
        try:
            Configuration.configure(self.config.store_id,
                                    self.config.the_secret_key)

            # payment = Payment.create({
            #     "amount": {
            #         "value": "150.00",
            #         "currency": "RUB"
            #     },
            #     "confirmation": {
            #         "type": "redirect",
            #         "return_url": self.config.URL_BOT
            #     },
            #     "capture": True,
            #     "description": "Оплата подписки"})
            payment = Payment.create({
                "amount": {
                    "value": "150.00",
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": self.config.URL_BOT
                },
                "capture": True,
                "description": "Оплата подписки",
                "receipt": {
                    "customer": {
                        "full_name": f"{full_name}",
                        "email": "test@gmail.com",
                        "phone": "+79309437105"
                    },
                    "items": [
                        {
                            "description": "Подписка в боте",
                            "quantity": "150.00",
                            "amount": {
                                "value": 1,
                                "currency": "RUB"
                            },
                            "vat_code": "2",
                            "payment_mode": "full_payment",
                            "payment_subject": "service",
                            "supplier": {
                                "name": "string",
                                "phone": "string"
                            }
                        },
                    ]
                }
            }
            )

            url = payment.confirmation.confirmation_url
            return payment.id, url
        except Exception as e:
            logging.exception(e, exc_info=True)
            return None, None

    async def __set_time_prediction(
            self,
            call: types.CallbackQuery,
            state: FSMContext
    ):
        col_info = self.operation_db.COLUMNS_INFO

        payments_end = self.operation_db.select_user_info_db(
            f"{col_info.referrals_count}, {col_info.payments_end}",
            call.message.from_user.id,
            many=True
        )
        if get_day_and_hours_from_date(payments_end) != 0:
            await call.message.answer(
                text="Введите время отправки прогноза на следующий день,\n"
                     "Обращаю внимание что время нужно указать по МСК в формате:"
                     "HH MM (часы, минуты)"
            )
            await state.set_state(states.set_time_prediction)
        else:
            await call.message.answer(
                text="У вас нет подписки для настройки авто предсказания.",
                reply_markup=self.keyboard.main_menu_kb
            )

    @staticmethod
    def check_user_payments(payment_id) -> bool:
        try:
            payment = Payment.find_one(payment_id)
            if payment.status == "succeeded":
                return True
            else:
                return False
        except:
            return False

    async def start_payments(self, call: types.CallbackQuery):
        col_info = self.operation_db.COLUMNS_INFO

        referrals_count, payments_id = self.operation_db.select_user_info_db(
            f"{col_info.referrals_count}, {col_info.payments_id}",
            call.from_user.id,
            many=True
        )

        if await self.__check_and_update_info_payments(payments_id, call):
            return

        await call.message.answer(
            text="""✨ Наш бот создан, чтобы делиться магией астрологии с тобой совершенно бесплатно! 💫

Ты можешь получить доступ к ежедневным прогнозам двумя способами:
🔹 Пригласи 2 друзей — просто отправь им свою реферальную ссылку, и когда они сделают первую генерацию, подписка активируется! 🎁
🔹 Оформи подписку за 150₽ — это символический вклад, который помогает поддерживать работу бота и покрывать расходы на обслуживание.

Мы с любовью развиваем этот проект, чтобы ты мог получать точные персональные прогнозы. 💖 Выбери удобный способ и продолжай наслаждаться магией звёзд! ✨""",
            reply_markup=self.keyboard.payments_choice_ikb,
        )

    async def choice_payments(self, call: types.CallbackQuery):
        _, choice = call.data.split("_", maxsplit=1)

        col_info = self.operation_db.COLUMNS_INFO

        referrals_count = self.operation_db.select_user_info_db(
            col_info.referrals_count,
            call.from_user.id,
        )

        if choice == "point":
            if referrals_count >= 2:
                await call.message.answer(
                    text=f"Вам хватает реферальных баллов для оплаты подписки "
                         f"(спишется 2 реферальных балла), оплачиваем подписку?",
                    reply_markup=self.keyboard.ref_payments_ikb,
                )
            else:
                pay_id, url = self.__create_payments(call.from_user.full_name)

                if pay_id is None:
                    return

                self.operation_db.update_user_info_db(
                    {
                        col_info.payments_id: pay_id
                    },
                    call.from_user.id
                )
                await call.message.answer(
                    text="У вас не хватает реферальных баллов для оплаты "
                         f"подписки, (у вас {referrals_count} баллов, для оплаты "
                         f"нужно 2 балла), но вы можете приобрести подписку за "
                         f"150руб.",
                    reply_markup=self.keyboard.create_payments_ikb(
                        url=url,
                        id=pay_id,
                    ),
                )
        else:
            pay_id, url = self.__create_payments(call.from_user.full_name)

            if pay_id is None:
                return

            self.operation_db.update_user_info_db(
                {
                    col_info.payments_id: pay_id
                },
                call.from_user.id
            )

            await call.message.answer(
                text=f"Оплата подписки на месяц стоит 150 руб.",
                reply_markup=self.keyboard.create_payments_ikb(
                    url=url,
                    id=pay_id,
                ),
            )

    async def ref_payments(self, call: types.CallbackQuery, state: FSMContext):
        col_info = self.operation_db.COLUMNS_INFO

        referrals_count, payments_end = self.operation_db.select_user_info_db(
            f"{col_info.referrals_count}, {col_info.payments_end}",
            call.message.from_user.id,
            many=True
        )

        self.operation_db.update_user_info_db(
            {
                col_info.payments_id: None,
                col_info.payments_end: create_new_payments_end(payments_end),
                col_info.referrals_count: referrals_count - 2,
                col_info.generation_count: 10
            },
            call.from_user.id
        )

        await call.message.answer(
            text="Вы успешно оплатили подписку за 2 реферальных балла",
            reply_markup=self.keyboard.main_menu_kb,
        )

        await self.__set_time_prediction(call, state)

    async def check_payments(self, call: types.CallbackQuery, state: FSMContext):
        _, id = call.data.split("_", maxsplit=1)

        if self.check_user_payments(id):
            col_info = self.operation_db.COLUMNS_INFO
            payments_end = self.operation_db.select_user_info_db(
                col_info.payments_end,
                call.from_user.id
            )
            new_pay_end_date = create_new_payments_end(payments_end)

            self.operation_db.update_user_info_db(
                {
                    col_info.payments_id: None,
                    col_info.payments_end: new_pay_end_date,
                    col_info.generation_count: 10
                },
                call.from_user.id
            )

            await call.message.answer(
                text="Вы успешно оплатили подписку",
                reply_markup=self.keyboard.main_menu_kb,
            )

            await self.__set_time_prediction(call, state)
        else:
            await call.answer(
                text="Вы не оплатили подписку!"
            )

    def create_router(self):
        self.router.callback_query.register(self.start_payments,
                                     F.data == "payments")
        self.router.callback_query.register(
            self.check_payments,
            F.data.split("_")[0] == "check payment"
        )
        self.router.callback_query.register(
            self.ref_payments,
            F.data == "ref payments"
        )
        self.router.callback_query.register(
            self.choice_payments,
            F.data.split("_")[0] == "choice payments"
        )
        self.router.callback_query.register(
            self.__set_time_prediction,
            F.data == "set time prediction"
        )