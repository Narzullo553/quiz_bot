from aiogram import types

from loader import dp, db, bot


@dp.message_handler(lambda message: "/Barchaga_habar" in message.text)
async def foydalanuvchilarga_habar(msg: types.Message):
    try:
        text = msg.text.replace("/Barchaga_habar", '')
        datas = db.select_all_users()
        for data in datas:
            tg_id = data[2]
            name = data[1]
            try:
                if not text:
                    text = (f"Salom {name} bot qayta yuklandi"
                            f"/start ni bosib davom eting")
                await bot.send_message(chat_id=tg_id, text=text)
            except:
                pass
    except Exception as e:
        await msg.answer(text=f"barchaga habar: {e}")