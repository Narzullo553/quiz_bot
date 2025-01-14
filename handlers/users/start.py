from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from keyboards.default.bosh_menu import main_menu
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer("Assalomu alaykum \nbo'limlardan birini tanlang!!",
                         reply_markup=main_menu)
