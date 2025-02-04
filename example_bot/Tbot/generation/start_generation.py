from aiogram import types
from aiogram.fsm.context import FSMContext

from . import AllTypesGeneration
from example_bot.Tbot import BasicBotOperation


class StartAllGeneration(BasicBotOperation):
    # Начало любой генерации

    async def start_generation(
            self,
            message_or_call: types.Message or types.CallbackQuery,
            state: FSMContext):
        col_info = self.operation_db.COLUMNS_INFO

        userid = message_or_call.from_user.id

        if isinstance(message_or_call, types.Message):
            text_correct = message_or_call.text
            answer = message_or_call.answer
        else:
            text_correct = message_or_call.data
            answer = message_or_call.message.answer
            await state.update_data(period=text_correct.split("_")[-1])

        count_generation, referral_user, generation_count_all = \
            self.operation_db.select_user_info_db(
                f"{col_info.generation_count}, "
                f"{col_info.referral_user},"
                f"{col_info.generation_count_all}",
                userid,
                many=True
            )

        if generation_count_all == 0:
            if referral_user:
                referrals_count, referral_all_count_points_user = \
                    self.operation_db.select_user_info_db(
                        f"{col_info.referrals_count}, "
                        f"{col_info.referral_all_count_points_user}",
                        referral_user,
                        many=True
                    )
                self.operation_db.update_user_info_db(
                    {
                        col_info.referrals_count: referrals_count + 1,
                        col_info.referral_all_count_points_user:
                            referral_all_count_points_user + 1,
                    },
                    referral_user
                )
                self.operation_db.update_user_info_db(
                    {
                        col_info.referral_user: None
                    },
                    userid
                )

        if count_generation > 0:
            place_birth = self.operation_db.select_user_info_db(
                col_info.place_birth,
                userid,
            )
            if place_birth:
                text = """🔮 Готовы к новому прогнозу? Вы можете использовать уже сохранённые результаты или ввести новые данные, если что-то изменилось.

📂 Использовать предыдущие данные — быстрый способ получить прогноз на основе уже введённой информации. Если ваши данные актуальны, просто выберите этот вариант.

✍️ Ввести новые данные — если хотите обновить дату, время или место рождения. ⚠️ Обратите внимание: новые данные заменят старые и будут использоваться для всех прогнозов, включая ежедневные. 
❌ Отменить генерацию — если передумали или хотите вернуться назад.

✨ Выбирайте удобный вариант, и мы двигаемся дальше! 🚀"""
                keyboard = self.keyboard.start_generation_ikb
                await state.set_state(AllTypesGeneration()[text_correct])
            else:
                text = "Перед началом генерации нужно ввести ваши данные."
                keyboard = self.keyboard.no_generation_data_ikb
                await state.clear()

        elif userid in self.config.ADMINS_ID and \
                count_generation <= 0:
            self.operation_db.update_user_info_db(
                {
                    col_info.generation_count: 4
                },
                userid,
            )
            text = ("Я узнал вас администратор, обновляю ваши генерации. Можете продолжать.")
            keyboard = self.keyboard.start_generation_ikb
            await state.set_state(AllTypesGeneration()[text_correct])

        else:
            text = ("Вы использовали все доступные генерации. "
                    "Новые генерации будут доступны завтра в 00:00 по МСК.")
            keyboard = self.keyboard.main_menu_kb
            await state.clear()

        await answer(
            text=text,
            reply_markup=keyboard
        )

    def create_router(self):
        self.router.message.register(
            self.start_generation,
            AllTypesGeneration()
        )
        self.router.callback_query.register(
            self.start_generation,
            AllTypesGeneration()
        )
