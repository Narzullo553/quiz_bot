from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db, bot
import json


@dp.callback_query_handler(lambda call: "javob_qidir:" in call.data)
async def javob_qidir(call: types.CallbackQuery, state: FSMContext):
    try:
        _, nom, tg_id = call.data.split(":")
        await call.message.delete()
        await state.set_state("javob_qidir")
        await state.update_data({'nom': nom,'tg_id': tg_id})
        await call.message.answer(text="savolni kiriting")
    except:
        return 

@dp.message_handler(state="javob_qidir")
async def javob_qidirish(msg: types.Message, state: FSMContext):
    try:
        datas = await state.get_data()
        nom = datas['nom']
        tg_id = datas['tg_id']
        data = db.select_tests(telegram_id=int(tg_id), test_nomi=nom)
        data = data[0]
        data = json.loads(data)
        question = list(data.values())
        for i in question:
            for text, savol in i.items():
                if msg.text.lower() in text.lower():
                    try:
                        await msg.answer(text=f"savol: {text}"
                                              f"\njavob: {savol['#'][0]}")
                    except:
                        await msg.answer(text=f"savol: {text}"
                                              f"\nxatolar: {savol['+']}")
    except:
        pass



