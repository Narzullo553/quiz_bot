from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from keyboards.default.bosh_menu import bosh_menu
from keyboards.default.zamdekan_uchun_tugmalar import zamdekan_menu
from loader import dp, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if str(message.from_user.id) not in ADMINS:
        await message.answer(f"Salom! 🌟 {message.from_user.full_name} xush kelibsiz! "
                             f"Sizga qanday yordam bera olishim mumkin? ", reply_markup=bosh_menu)
    else:
        await message.answer("Assalomu alaykum \nbo'limlardan birini tanlang!!",
                             reply_markup=zamdekan_menu)
