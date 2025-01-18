from os import urandom

from aiogram import types

from data.config import ADMINS
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

"""testni boshlash qismi"""
async def testni_boshlash1(call, tg_id=None, nom=None):
    try:
        if tg_id is None:
            tg_id = call.from_user.id
            nom = call.data.replace('boshlash_1:', '')
        await call.message.delete()
        user_data[call.from_user.id] = user_data.get(call.from_user.id, {})
        user_data[call.from_user.id][call.from_user.id] = {'raqam': 1, 'xatolar': [], 'db_test_id':tg_id, 'nom': nom}
        await send_question(tg_id=call.from_user.id)
    except:
         return

@dp.callback_query_handler(lambda call: "boshlash_1:" in call.data)
async def testni_boshlash12(call: types.CallbackQuery):
    await testni_boshlash1(call)



async def send_question(tg_id, text1 = None, test_id=None):
    try:
        user_sessions_for_chat = user_data.get(tg_id, {})
        if test_id is None:
            test_id = tg_id
        user = user_sessions_for_chat.get(test_id, 0)
        question_number = user['raqam']
        user_id = user['db_test_id']
        nom = user['nom']
        tg_id = int(tg_id)
        user_id = int(user_id)
        data = await db.select_tests(telegram_id=user_id, test_nomi=nom)
        data = data[0]
        data = json.loads(data)
        question = data[f'{question_number}']
        if text1 is None:
            text1 = ''
        else:
            if text1 == "Noto‘g‘ri javob! ❌":
                question1 = data[f'{question_number-1}']
                javob = list(question1.values())
                text1 += f"\nto'g'ri javob: {javob[0]['#'][0]}\n"
        if question_number < len(data):
            for text,question in question.items():
                try:
                    javoblar = list(set(question['#']+question['+']))
                    msg = await bot.send_poll(
                        chat_id=tg_id,
                        question=text,
                        options=javoblar,
                        type="quiz",
                        correct_option_id=javoblar.index(question['#'][0]),
                        is_anonymous=False
                    )

                    try:
                        a = msg.poll.id
                        del user_data[tg_id][test_id]
                        user['javob_id'] = javoblar.index(question['#'][0])
                        user['uzunlik'] = len(data)
                        user_data[tg_id][a] = user
                    except Exception as e:
                        await bot.send_message(chat_id=tg_id, text="Viktorina tugadi!")
                except Exception as e:
                    user_data[tg_id][test_id]['raqam'] += 1
                    await send_question(tg_id=tg_id, test_id=test_id)
        else:
            await bot.send_message(chat_id=tg_id, text="Viktorina tugadi!"
                                                         f"xatolar {user['xatolar']}")
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0], text=e)


@dp.poll_answer_handler()
async def process_poll_answer(poll_answer: types.PollAnswer):
    chat_id = poll_answer.user.id
    test_id = poll_answer.poll_id
    user_sessions_for_chat = user_data.get(chat_id, {})
    current_question = user_sessions_for_chat.get(test_id, 0)
    current_question_index = current_question['raqam']
    question_id = current_question['javob_id']
    uzunlik = current_question['uzunlik']

    if poll_answer.option_ids != [question_id]:
        if current_question:
            user_data[chat_id][test_id]['xatolar'].append(current_question_index)

    current_question_index += 1
    user_sessions_for_chat[test_id]['raqam'] = current_question_index
    if current_question_index < uzunlik:
        await send_question(chat_id, test_id=test_id)
    else:
        await bot.send_message(chat_id=chat_id, text="Viktorina tugadi!")





