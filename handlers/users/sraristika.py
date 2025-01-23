from aiogram import types

from filters import IsPrivate
from loader import dp, db


@dp.message_handler(IsPrivate(), text="📊 Statistika")
async def statistika(msg: types.Message):
    count = db.select_count_users()
    text = (f"Hozirgi kunda telegram botimizda"
            f"\n{count[0]} 👤 foydalanuvchi mavjud")
    await msg.answer(text=text)