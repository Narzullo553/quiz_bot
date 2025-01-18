
from aiogram import types
from filters import IsPrivate
from loader import dp, db, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
user_data = {}
async def testlarim(msg):
    try:
        tg_id = msg.from_user.id
        testlar = await db.search_tests(tg_id)
        if testlar:
            create_quiz_menu1 = InlineKeyboardMarkup(row_width=1)
            for nomi in testlar:
                create_quiz_menu1.add(InlineKeyboardButton(text=nomi['test_nomi'],
                                                           callback_data=f"test:{nomi['test_nomi']}"))
            await msg.answer(text="📋 Testlar ro'yhati", reply_markup=create_quiz_menu1)
        else:
            await msg.answer(text="Hali sizda testlar mavjud emas")
    except:
        return

@dp.message_handler(IsPrivate(),text="📋 Testlarim")
async def testlar(msg: types.Message):
    await testlarim(msg)

@dp.callback_query_handler(lambda call: "⬅️ ortga:" in call.data)
async def testlar1(call: types.CallbackQuery):
    try:
        tg_id = call.from_user.id
        testlar = await db.search_tests(tg_id)
        await call.message.delete()
        if testlar:
            create_quiz_menu1 = InlineKeyboardMarkup(row_width=1)
            for nomi in testlar:
                create_quiz_menu1.add(InlineKeyboardButton(text=nomi['test_nomi'],
                                                           callback_data=f"test:{nomi['test_nomi']}"))
            await call.message.answer(text="Testlardan ro'yhati", reply_markup=create_quiz_menu1)
        else:
            await call.message.answer(text="Hali sizda testlar mavjud emas")

    except:
        return
@dp.callback_query_handler(lambda call: "test:" in call.data)
async def testni_kor(call: types.CallbackQuery):
    try:
        nom = call.data.replace('test:', '')
        create_quiz_menu1 = InlineKeyboardMarkup(row_width=1)
        await call.message.delete()
        create_quiz_menu1.add(InlineKeyboardButton(text="⬅️ ortga", callback_data="ortga:a"))
        create_quiz_menu1.add(InlineKeyboardButton(text="🗑️❌ o'chirish", callback_data=f"ochir:{nom}"))
        create_quiz_menu1.add(InlineKeyboardButton(text="📝 Start", callback_data=f"boshlash_1:{nom}"))
        await call.message.answer(text=f"Testni boshlash uchun"
                                                        "\ntestni boshlash tugmasini bosing", reply_markup=create_quiz_menu1)
    except:
        return

@dp.callback_query_handler(lambda call: "ochir:" in call.data)
async def ochir(call: types.CallbackQuery):
    try:
        nom = call.data.replace('ochir:', '')
        await db.delete_tests(call.from_user.id, nom)
        await call.message.delete()
        await call.message.answer("test o'chirildi")
    except:
        return


async def testni_boshlash1(call, tg_id=None, nom=None):
    try:
        if tg_id is None:
            tg_id = call.from_user.id
            nom = call.data.replace('boshlash_1:', '')
        await call.message.delete()
        user_data[f"{call.from_user.id}:{nom}"] = {"score": 0, "current_question": 1, 'xatolar': []}
        await send_question(tg_id=call.from_user.id,nom=nom, user_id=tg_id)
    except:
         return

@dp.callback_query_handler(lambda call: "boshlash_1:" in call.data)
async def testni_boshlash12(call: types.CallbackQuery):
    await testni_boshlash1(call)



async def send_question(tg_id,user_id, nom, text1 = None):
    try:
        tg_id = int(tg_id)
        user_id = int(user_id)
        data = await db.select_tests(telegram_id=user_id, test_nomi=nom)
        data = data[0]
        data = json.loads(data)
        try:
            user = user_data[f"{tg_id}:{nom}"]
        except:
            user_data[f"{tg_id}:{nom}"] = {"score": 0, "current_question": 1, 'xatolar': []}
            user = user_data[f"{tg_id}:{nom}"]
        question_number = user["current_question"]
        question = data[f'{question_number}']
        markup = InlineKeyboardMarkup(row_width=1)
        if text1 is None:
            text1 = ''
        else:
            if text1 == "Noto‘g‘ri javob! ❌":
                question1 = data[f'{question_number-1}']
                javob = list(question1.values())
                text1 += f"\nto'g'ri javob: {javob[0]['#'][0]}\n"
        for text,question in question.items():
            try:
                javoblar = list(set(question['#']+question['+']))
                s = 0
                for option in javoblar:
                    if option == question['#'][0]:
                        cuurent = 1
                    else:
                        cuurent = 0
                        s += 1
                    markup.add(InlineKeyboardButton(option, callback_data=f"m:{question_number}:{cuurent}:{user_id}:{len(data)}:{nom}"))
                markup.add(InlineKeyboardButton("🛑 Stop", callback_data=f"stop_tests:{user_id}:{nom}"))
                await bot.send_message(tg_id, f"{text1} \nsavol: {question_number}. {text}", reply_markup=markup)
            except:
                user_data[f"{tg_id}:{nom}"]['current_question'] += 1
                await send_question(tg_id, user_id, nom, text1)
    except Exception as e:
        print('e',e)

@dp.callback_query_handler(lambda c: c.data.startswith("stop_tests:"))
async def quiz_test_stop(callback: types.CallbackQuery):
    try:
        _,user_id,nom = callback.data.split(":")
        try:
            user = user_data[f"{callback.from_user.id}:{nom}"]
        except:
            user_data[f"{callback.from_user.id}:{nom}"] = {"score": 0, "current_question": 1, 'xatolar': []}
            user = user_data[f"{callback.from_user.id}:{nom}"]
        soz = ""
        data = await db.select_tests(telegram_id=int(user_id), test_nomi=nom)
        data = data[0]
        data = json.loads(data)
        for i in user['xatolar']:
            question = data[f'{i}']
            for text, question in question.items():
                soz += (f"savol {i}: {text}"
                        f"\njavob: {question['#'][0]}\n\n")

        del user_data[f"{callback.from_user.id}:{nom}"]
        await callback.message.delete()
        await bot.send_message(callback.from_user.id,
                               f"Test tugadi! Sizning natijangiz: {user['score']}/{len(data)} 🎉"
                               f"\nxatolar:"
                               f"\n{soz}")
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda c: c.data.startswith("m:"))
async def quiz_callback_handler(callback: types.CallbackQuery):
    try:
        _, question_number, correct, user_id, l, nom= callback.data.split(":")
        question_number = int(question_number)
        user = user_data[f"{callback.from_user.id}:{nom}"]
        if int(correct):
            soz = "To'gri 🎯\n"
            user["score"] += 1
        else:
            user_data[f"{callback.from_user.id}:{nom}"]['xatolar'].append(question_number)
            soz = "Noto‘g‘ri javob! ❌"
        await callback.message.delete()
        if question_number < int(l):
            user["current_question"] += 1
            await send_question(callback.from_user.id,int(user_id),nom, text1=soz)
        else:
            soz = ""
            data = await db.select_tests(telegram_id=int(user_id), test_nomi=nom)
            data = data[0]
            data = json.loads(data)
            for i in user['xatolar']:
                question = data[f'{i}']
                for text, question in question.items():
                    soz += (f"savol {i}: {text}"
                            f"\njavob: {question['#'][0]}\n\n")

            del user_data[f"{callback.from_user.id}:{nom}"]
            await bot.send_message(callback.from_user.id,
                                   f"Test tugadi! Sizning natijangiz: {user['score']}/{l} 🎉"
                                   f"\nxatolar:"
                                   f"\n{soz}")
    except:
        return



