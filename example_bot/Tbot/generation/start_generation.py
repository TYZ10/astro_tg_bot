from aiogram import types
from aiogram.fsm.context import FSMContext

from . import AllTypesGeneration
from example_bot.Tbot import BasicBotOperation


class StartAllGeneration(BasicBotOperation):
    # Начало любой генерации

    async def start_generation(self,
                               message: types.Message,
                               state: FSMContext):
        col_info = self.operation_db.COLUMNS_INFO

        count_generation, referral_user, generation_count_all = \
            self.operation_db.select_user_info_db(
                f"{col_info.generation_count}, "
                f"{col_info.referral_user},"
                f"{col_info.generation_count_all}",
                message.from_user.id,
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
                    message.from_user.id
                )

        if count_generation > 0:
            place_birth = self.operation_db.select_user_info_db(
                col_info.place_birth,
                message.from_user.id,
            )
            if place_birth:
                text = """🔮 Готовы к новому прогнозу? Вы можете использовать уже сохранённые результаты или ввести новые данные, если что-то изменилось.

📂 Использовать предыдущие данные — быстрый способ получить прогноз на основе уже введённой информации.
✍️ Ввести новые данные — если хотите обновить дату, время или место рождения для более точного расчёта.
❌ Отменить генерацию — если передумали или хотите вернуться назад.

Выбирайте удобный вариант и двигаемся дальше! ✨"""
                keyboard = self.keyboard.start_generation_ikb
                await state.set_state(AllTypesGeneration()[message.text])
            else:
                text = "Перед началом генерации нужно ввести ваши данные."
                keyboard = self.keyboard.no_generation_data_ikb
                await state.clear()

        elif message.from_user.id in self.config.ADMINS_ID and \
                count_generation > 0:
            self.operation_db.update_user_info_db(
                {
                    col_info.generation_count: 4
                },
                userid=message.from_user.id,
            )
            text = ("Я узнал вас администратор, обновляю ваши генерации. Можете проболжать.")
            keyboard = self.keyboard.start_generation_ikb
            await state.set_state(AllTypesGeneration()[message.text])

        else:
            text = ("Вы использовали все доступные генерации. "
                    "Новые генерации будут доступны завтра в 00:00 по МСК.")
            keyboard = self.keyboard.main_menu_kb
            await state.clear()

        await message.answer(
            text=text,
            reply_markup=keyboard
        )

    def create_router(self):
        self.router.message.register(
            self.start_generation,
            AllTypesGeneration()
        )
