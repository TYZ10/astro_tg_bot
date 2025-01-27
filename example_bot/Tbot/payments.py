from aiogram import types, F
from aiogram.fsm.context import FSMContext
from yookassa import Payment

from . import BasicBotOperation
from example_bot.misc.datetime_function import create_new_payments_end


class PaymentsBot(BasicBotOperation):

    async def __check_and_update_info_payments(self, payments_id,
                                       message: types.Message):
        col_info = self.operation_db.COLUMNS_INFO

        if payments_id:
            if self.check_user_payments(payments_id):
                payments_end = self.operation_db.select_user_info_db(
                    col_info.payments_end,
                    message.from_user.id
                )
                new_pay_end_date = create_new_payments_end(payments_end)

                self.operation_db.update_user_info_db(
                    {
                        col_info.payments_id: None,
                        col_info.payments_end: new_pay_end_date
                    },
                    message.from_user.id
                )

                await message.answer(
                    text="Я заметил не проверенную вами оплату подписки, "
                         "продлеваю вашу подписку.",
                    reply_markup=self.keyboard.main_menu_ikb,
                )
                return True
            else:
                self.operation_db.update_user_info_db(
                    {
                        col_info.payments_id: None
                    },
                    message.from_user.id
                )

    def __create_payments(self):
        """Создание оплаты"""

        #  https://yookassa.ru/developers/api#payment_object
        #  https://yookassa.ru/developers/api#create_payment

        payment = Payment.create({
            "amount": {
                "value": "250.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": self.config.URL_BOT
            },
            "capture": True,
            "description": "Оплата подписки"})

        url = payment.confirmation.confirmation_url
        return payment.id, url

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

    async def start_payments(self, message: types.Message):
        col_info = self.operation_db.COLUMNS_INFO

        referrals_count, payments_id = self.operation_db.select_user_info_db(
            f"{col_info.referrals_count}, {col_info.payments_id}",
            message.from_user.id,
            many=True
        )

        if await self.__check_and_update_info_payments(payments_id, message):
            return

        if referrals_count >= 2:
            await message.answer(
                text=f"Вам хватает реферальных баллов для оплаты подписки "
                     f"(спишется 2 реферальных балла), оплачиваем подписку?",
                reply_markup=self.keyboard.ref_payments_ikb,
            )
        else:
            pay_id, url = self.__create_payments()

            self.operation_db.update_user_info_db(
                {
                    col_info.payments_id: pay_id
                },
                message.from_user.id
            )

            await message.answer(
                text=f"У вас не хватает реферальных баллов для оплаты "
                     f"подписки, (у вас {referrals_count} баллов, для оплаты "
                     f"нужно 2 балла), поэтому можете приобрести подписку за "
                     f"250руб. (в случае если вы оплатите и забудете "
                     f"проверить бот сам проверит оплатили ли вы или нет "
                     f"при следующей попытке)",
                reply_markup=self.keyboard.create_payments_ikb(
                    url=url,
                    id=pay_id,
                ),
            )

    async def start_payments_call(self, call: types.CallbackQuery):
        await self.start_payments(call.message)

    async def ref_payments(self, call: types.CallbackQuery):
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
            },
            call.from_user.id
        )

        await call.message.answer(
            text="Вы успешно оплатили подписку за 2 реферальных балла",
            reply_markup=self.keyboard.main_menu_ikb,
        )

    async def check_payments(self, call: types.CallbackQuery):
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
                    col_info.payments_end: new_pay_end_date
                },
                call.from_user.id
            )

            await call.message.answer(
                text="Вы успешно оплатили подписку",
                reply_markup=self.keyboard.main_menu_ikb,
            )
        else:
            await call.answer(
                text="Вы не оплатили подписку!"
            )

    def create_router(self):
        self.router.message.register(self.start_payments,
                                     F.text == "Оплата подписки")
        self.router.message.register(self.start_payments_call,
                                     F.data == "payments")
        self.router.callback_query.register(
            self.check_payments,
            F.data.split("_")[0] == "check payment"
        )
        self.router.callback_query.register(
            self.ref_payments,
            F.data == "ref payments"
        )