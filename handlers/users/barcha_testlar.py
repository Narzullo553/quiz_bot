from aiogram import types
from filters import IsPrivate
from handlers.users.testlarim import testni_boshlash1
from loader import dp, db, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
@dp.callback_query_handler(lambda call: "ortga_barcha:" in call.data)
async def testlar_barcha_ortga1(call: types.CallbackQuery):
    await call.message.delete()
    test = await testlarim_xammasi()
    if test:
        await call.message.answer(text="📋 Testlar ro'yhati", reply_markup=test)

    else:
        await call.message.answer(text="Hali sizda testlar mavjud emas")


async def testlarim_xammasi(page=1):
    try:
        testlar = await db.select_all_tests(page=page)
        if testlar:
            create_quiz_menu1 = InlineKeyboardMarkup(row_width=1)
            for nomi in testlar:
                create_quiz_menu1.add(InlineKeyboardButton(text=nomi['test_nomi'],
                                                           callback_data=f"test123:{nomi['test_nomi']}:{nomi['telegram_id']}"))
            uzunlik = await db.test_count()
            if int(uzunlik) > 10:
                if page != 1:
                    if page*10 != int(uzunlik):
                        create_quiz_menu1.add(InlineKeyboardButton(text="🔙 Orqaga",
                                                                   callback_data=f"page:{page-1}"))
                        create_quiz_menu1.add(InlineKeyboardButton(text="Oldinga 🔜",
                                                                   callback_data=f"page:{page+1}"))
                    else:
                        create_quiz_menu1.add(InlineKeyboardButton(text="🔙 Orqaga",
                                                                   callback_data=f"page:{page-1}"))
                else:
                    create_quiz_menu1.add(InlineKeyboardButton(text="Oldinga 🔜",
                                                               callback_data=f"page:{page+1}"))

            return create_quiz_menu1
        else:
            return ''
    except:
        return

@dp.message_handler(IsPrivate(),text="🔍 Testlarni o‘rganish")
async def testlar(msg: types.Message):
    test = await testlarim_xammasi()
    if test:
        await msg.answer(text="📋 Testlar ro'yhati", reply_markup=test)

    else:
        await msg.answer(text="Hali sizda testlar mavjud emas")

@dp.callback_query_handler(lambda call: "page:" in call.data)
async def testlar1(call: types.CallbackQuery):
    page = int(call.data.replace('page:', ''))
    test = await testlarim_xammasi(page=page)
    if test:
        await call.message.answer(text="📋 Testlar ro'yhati", reply_markup=test)

    else:
        await call.message.answer(text="Hali sizda testlar mavjud emas")

@dp.callback_query_handler(lambda call: "test123:" in call.data)
async def testni_korish(call: types.CallbackQuery):
    try:
        _, nomi, tg_id = call.data.split(":")
        create_quiz_menu1 = InlineKeyboardMarkup(row_width=1)
        await call.message.delete()
        create_quiz_menu1.add(InlineKeyboardButton(text="⬅️ ortga", callback_data=f"ortga_barcha:{nomi}:{tg_id}"))
        create_quiz_menu1.add(InlineKeyboardButton(text="📝 Start", callback_data=f"boshlash_barcha:{nomi}:{tg_id}"))
        await call.message.answer(text=f"Testni boshlash uchun"
                                                        "\ntestni boshlash tugmasini bosing", reply_markup=create_quiz_menu1)
    except:
        return

@dp.callback_query_handler(lambda call: "boshlash_barcha:" in call.data)
async def testni_boshlash_barcha(call: types.CallbackQuery):
    _, nomi, tg_id = call.data.split(":")
    await testni_boshlash1(call=call, nom=nomi, tg_id=tg_id)