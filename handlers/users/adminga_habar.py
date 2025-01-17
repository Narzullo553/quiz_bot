from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from filters import IsPrivate
from loader import dp, db, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



@dp.callback_query_handler(lambda call: "adminga_yoz" in call.data)
async def adminga_habar(call: types.CallbackQuery, state: FSMContext):
    try:
        text = "Iltimos, adminga yozmoqchi bo'lgan xabaringizni yuboring 📩💬"
        tugma = InlineKeyboardMarkup(row_width=1)
        tugma.add(InlineKeyboardButton(text="🛑 Stop", callback_data="cancel"))
        await call.message.delete()
        msg = await call.message.answer(text=text, reply_markup=tugma)
        await state.update_data({'msg': msg})
        await state.set_state('adminga habar yubor')
    except:
        return

@dp.message_handler(IsPrivate(), state='adminga habar yubor')
async def adminga_habar_yubor(msg: types.Message, state: FSMContext):
    try:
        admin = int(ADMINS[0])
        data = await state.get_data()
        print(data)
        msge = data['msg']
        await msg.answer("xabaringiz adminga yuborildi")
        await msge.delete()
        tugma = InlineKeyboardMarkup(row_width=1)
        tugma.add(InlineKeyboardButton(text="javob yozish", callback_data="javob_yubor"))
        await bot.send_message(admin, f"Foydalanuvchidan yangi xabar:\n\n{msg.text}"
                                      f"\nnime: {msg.from_user.full_name}"
                                      f"\ntelegram id: {msg.from_user.id}")
        await state.finish()
    except Exception as e:
        print(e)

@dp.message_handler(IsPrivate(), text="📞 Qo'llab-quvvatlash")
async def Qollab_quvvatlash(msg: types.Message):
    await msg.delete()
    matn ="""💬 **Qo‘llab-quvvatlash bo‘limi**
    Agar sizga yordam kerak bo‘lsa yoki botning ishlashida qandaydir muammo yuzaga kelsa, bizga quyidagi usullardan birida murojaat qilishingiz mumkin:
    - 🤖 Bot haqida savollar yoki yordam.
    - 🐞 Xatolik yoki nosozliklarni bildirish.
    - 🔄 Botda xato ishlash holatlari.
    - ⚙️ Botni ishlatishda qayd etilgan muammolar.

    👇 Quyida "Yordam" tugmasini bosing va bizga murojaat qiling."""

    tugma = InlineKeyboardMarkup(row_width=1)
    tugma.add(InlineKeyboardButton(text="👨‍💻 – yozish", callback_data="adminga_yoz"))
    await msg.answer(text=matn, reply_markup=tugma)
