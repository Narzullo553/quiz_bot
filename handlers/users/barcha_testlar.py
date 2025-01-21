from aiogram import types
from data.config import ADMINS
from filters import IsPrivate
from handlers.users.testlarim import testni_boshlash1
from loader import dp, db, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@dp.callback_query_handler(lambda call: "ortga_barcha:" in call.data)
async def testlar_barcha_ortga1(call: types.CallbackQuery):
    try:
        text, test, db_id = await testlarim_xammasi()
        if test:
            await call.message.delete()
            await call.message.answer(text=f"📋 {text}", reply_markup=test)

        else:
            await call.message.answer(text="Hali sizda testlar mavjud emas")
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0], text=f"ortga_barcha: {e}")



async def testlarim_xammasi(page=1, db_id=5):
    try:
        if db_id == 5:
            uzunlik = await db.test_count()
        else:
            uzunlik = await db.test_count1(int(db_id))
        if uzunlik+10 - page*10 >=0:
            if db_id == 5:
                testlar = await db.select_all_tests(page=page)
            else:
                testlar = await db.select_all_tests1(page=page, telegram_id=db_id)
        else:
            testlar = None
        if testlar:
            create_quiz_menu1 = InlineKeyboardMarkup(row_width=5)
            s = page*10-10+1
            text = f"Testlar ro'yhati {s}-{page*10}: {uzunlik}"
            for son, nomi in enumerate(testlar, start=1):
                text += '\n' + f"{son}. {nomi['test_nomi']}"
                create_quiz_menu1.insert(InlineKeyboardButton(text=f"{son}",
                                                           callback_data=f"test123:{nomi['test_nomi']}:{nomi['telegram_id']}:{db_id}"))

            create_quiz_menu1.row(
                InlineKeyboardButton("◀", callback_data=f"page:{page-1}:{db_id}"),
                InlineKeyboardButton("❌", callback_data="cancel"),
                InlineKeyboardButton("▶", callback_data=f"page:{page+1}:{db_id}"),
            )
            return text, create_quiz_menu1,db_id
        else:
            return '', '', '',
    except:
        return

@dp.callback_query_handler(lambda call: "cancel" in call.data)
async def ochirish(call: types.CallbackQuery):
    try:
        await call.message.delete()
    except:
        pass

@dp.message_handler(IsPrivate(),text="🔍 Testlarni o‘rganish")
async def testlar(msg: types.Message):
    try:
        if msg.from_user.id in [5609632063, 6558804634, 5650754343,
                                6314174940, 5088814012, 5898315957,
                                6480714798, 7848635964, 5161135228,
                                6392040618, 5862386592, 6205586837,
                                6371449408, 6943710922, 1427324085,
                                5746455715, 5036977201, 5084200014,
                                1290613174, 7209502121, 6680497047,
                                6110052788, 6105134239, 1513686261,
                                7133622536, 5161135228, 6371449408,
                                6418233942,int(ADMINS[0])
                                ]:
            text, test, db_id = await testlarim_xammasi()
            if test:
                await msg.answer(text=f"📋 {text}", reply_markup=test)

            else:
                await msg.answer(text="Testlar ro'yhati topilmadi")
        else:
            await msg.answer(text="Testlar ro'yhati topilmadi")
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0], text=f"test ro'yhati barcha: {e}")



@dp.callback_query_handler(lambda call: "page:" in call.data)
async def testlar1(call: types.CallbackQuery):
    try:
        _, page, db_id = call.data.split(":")
        if int(page) > 0:
            if int(db_id) != 5:
                text,test, db_id = await testlarim_xammasi(page=int(page))
            else:
                text, test, db_id = await testlarim_xammasi(page=int(page), db_id=int(db_id))
            if test:
                await call.message.delete()
                await call.message.answer(text=f"📋 {text}", reply_markup=test)
            else:
                await call.answer("testlar topilmadi")
        else:
            await call.answer("testlar topilmadi")

    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0], text=f"test ro'yhati: {e}")


@dp.callback_query_handler(lambda call: "test123:" in call.data)
async def testni_korish(call: types.CallbackQuery):
    try:
        _, nomi, tg_id, db_id = call.data.split(":")
        if int(db_id) != 5 or call.from_user.id == int(ADMINS[0]):
            create_quiz_menu1 = InlineKeyboardMarkup(row_width=2)
            create_quiz_menu1.insert(InlineKeyboardButton(text="🗑️❌ o'chirish", callback_data=f"ochir:{nomi}:{tg_id}"))
            create_quiz_menu1.insert(InlineKeyboardButton(text="📝 Start", callback_data=f"boshlash_1:{nomi}:{tg_id}"))
            await call.message.answer(text=f"Testni boshlash uchun"
                                           "\ntestni boshlash tugmasini bosing", reply_markup=create_quiz_menu1)
        else:
            await testni_boshlash_barcha(call, nomi=nomi, tg_id=int(tg_id))
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0], text=f"test ro'yhati: {e}")


async def testni_boshlash_barcha(call: types.CallbackQuery,nomi=None, tg_id=None):
    try:
        if nomi is None:
            _, nomi, tg_id = call.data.split(":")
        await testni_boshlash1(call=call, nom=nomi, tg_id=tg_id)
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0], text=f"test ro'yhati: {e}")

@dp.callback_query_handler(lambda call: "boshlash_barcha:" in call.data)
async def testni_boshlash_barcha1(call: types.CallbackQuery):
    await call.message.delete()
    await testni_boshlash_barcha(call=call)