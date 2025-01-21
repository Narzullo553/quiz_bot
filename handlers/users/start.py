from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default.bosh_menu import main_menu
from loader import dp, db
from aiogram.dispatcher import FSMContext


@dp.message_handler(text='/cancel', state='*')
async def bekor_qil(msg:types.Message, state: FSMContext):
    await msg.answer("jarayon yakunlandi")
    await msg.delete()
    await state.finish()

@dp.message_handler(CommandStart(),IsPrivate())
async def bot_start(message: types.Message):
    try:
        user = message.from_user
        m_user = await db.select_one_users(user.id)
        if m_user is None:
            await db.add_users(fullname=user.full_name, telegram_id=user.id)
    except Exception as err:
        print(err)
    await message.answer("Assalomu alaykum \nbo'limlardan birini tanlang!!",
                         reply_markup=main_menu)
