import asyncio
import re
import random as rn

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from filters import IsPrivate
from loader import dp, db, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
user_data = {}

async def clear():
    global user_data, active_polls
    user_data = {}
    active_polls = {}


@dp.callback_query_handler(lambda call: "soniyasiz:" in call.data)
async def Soniya3(call: types.CallbackQuery):
    _, nom, db_id = call.data.split(":")
    await testni_boshlash321(call=call, tg_id=int(db_id), nom=nom)


async def testni_boshlash321(call, tg_id=None, nom=None):
    try:
        if tg_id is None:
            tg_id = call.from_user.id
            nom = call.data.replace('boshlash_1:', '')
        user_data[call.from_user.id] = user_data.get(call.from_user.id, {})
        user_data[call.from_user.id][call.from_user.id] = {'raqam': 1, 'xatolar': [], 'db_test_id':tg_id, 'nom': nom}
        tugma = InlineKeyboardMarkup(row_width=1)
        tugma.add(InlineKeyboardButton(text="🔀 - Tasodifiy Test:", callback_data=f"random_test12"))
        tugma.add(InlineKeyboardButton(text="✅ - Oddiy Test:", callback_data=f"oddiy_test12"))
        await bot.send_message(chat_id=call.from_user.id,
                               text="Test qay tarzda o'tkazilsin", reply_markup=tugma)
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0], text=f"testni_boshlash1 {e}")


@dp.callback_query_handler(lambda call: "oddiy_test12" in call.data)
async def oddiy_test21(call: types.CallbackQuery):
    try:
        await call.message.delete()
        user_data[call.from_user.id][call.from_user.id]['test_turi'] = "oddiy_test"
        await send_question(tg_id=call.from_user.id)
    except:
        user_data[call.from_user.id] = user_data.get(call.from_user.id, {})
        test_id = ''
        for i, j in user_data[call.from_user.id].items():
            test_id = i
        user_data[call.from_user.id][test_id]['test_turi'] = "oddiy_test"
        await send_question(tg_id=call.from_user.id)

@dp.callback_query_handler(lambda call: "random_test12" in call.data)
async def random_test21(call: types.CallbackQuery, state: FSMContext):
    try:
        try:
            user_data[call.from_user.id][call.from_user.id]['test_turi'] = "random_test"
        except:
            user_data[call.from_user.id] = user_data.get(call.from_user.id, {})
            user_data[call.from_user.id][call.from_user.id]['test_turi'] = "random_test"
        datas = user_data[call.from_user.id][call.from_user.id]
        nom = datas['nom']
        db_id = datas['db_test_id']
        data = await db.select_tests(telegram_id=int(db_id), test_nomi=nom)
        data = data[0]
        data = json.loads(data)
        user_data[call.from_user.id][call.from_user.id]['uzunlik'] = len(data)
        text = ("test miqdori kiriting !!"
                f"\n{len(data)} dan kam miqdor kiriting"
                f"\nmisol: 20 ta"
                f"\n/cancel bekor qilish")
        await call.message.delete()
        await call.message.answer(text=text)
        await state.set_state('test_soni_yubor1')
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0], text=f"randomtest: {e}")

@dp.message_handler(state='test_soni_yubor1')
async def test_soni21(msg: types.Message, state: FSMContext):
    try:
        number = re.findall(r'\d+', msg.text)
        l = user_data[msg.from_user.id][msg.from_user.id]['uzunlik']
        if int(number[0]) > l:
            await msg.answer(f"iltimos {l} dan kam miqdor kiriting")
        else:
            numbers = rn.sample(range(1, l+1), int(number[0]))
            user_data[msg.from_user.id][msg.from_user.id]['sonlar'] = numbers
            user_data[msg.from_user.id][msg.from_user.id]['test_uzunligi'] = len(numbers)
            await state.finish()
            await send_question(tg_id=msg.from_user.id)
    except:
        await msg.answer(f"iltimos test miqdorini to'g'ri kiriting")



async def send_question(tg_id, test_id=None):
    try:
        user_sessions_for_chat = user_data.get(tg_id, {})
        if test_id is None:
            test_id = tg_id
        user = user_sessions_for_chat.get(test_id, 0)
        question_number = user['raqam']
        test_turi = user['test_turi']
        user_id = user['db_test_id']
        nom = user['nom']
        tg_id = int(tg_id)
        user_id = int(user_id)
        data = await db.select_tests(telegram_id=user_id, test_nomi=nom)
        data = data[0]
        data = json.loads(data)
        user_data[tg_id][test_id]['test_uzunligi1'] = len(data)
        if test_turi == "random_test":
            numbers = user['sonlar']
            question_number = numbers[0]
            question = data[f'{question_number}']
        else:
            question = data[f'{question_number}']

        if question_number <= len(data):
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
                    if test_turi == "random_test":
                        del user_data[tg_id][test_id]['sonlar'][0]
                        user_data[tg_id][test_id]['sonlar'].append(user_data[tg_id][test_id]['raqam'])
                    await send_question(tg_id=tg_id, test_id=test_id)
        else:
            del user_data[tg_id][test_id]
            await bot.send_message(chat_id=tg_id, text="Viktorina tugadi!"
                                                         f"xatolar {user['xatolar']}")
    except Exception as e:
        del user_data[tg_id][test_id]
        await bot.send_message(chat_id=ADMINS[0], text=f"send_questio {e}")




async def process_poll_answer1(poll_answer: types.PollAnswer):
    try:
        chat_id = poll_answer.user.id
        test_id = poll_answer.poll_id
        user_sessions_for_chat = user_data.get(chat_id, {})
        current_question = user_sessions_for_chat.get(test_id, 0)
        current_question_index = current_question['raqam']
        question_id = current_question['javob_id']
        uzunlik = current_question['test_uzunligi1']
        test_turi = user_data[poll_answer.user.id][test_id]['test_turi']
        if test_turi == "random_test":
            current_question_index = user_data[poll_answer.user.id][test_id]['sonlar'].pop(0)
        if poll_answer.option_ids != [question_id]:
            if current_question:
                user_data[chat_id][test_id]['xatolar'].append(current_question_index)
        current_question_index += 1
        user_sessions_for_chat[test_id]['raqam'] = current_question_index
        if test_turi == "random_test":
            if current_question['sonlar']:
                await send_question(chat_id, test_id=test_id)
            else:
                test_uzunligi = int(current_question['test_uzunligi'])
                xatolar_list = user_data[chat_id][test_id]['xatolar']
                xatolar = int(len(xatolar_list))
                nom = current_question['nom']
                db_test_id = current_question['db_test_id']
                del user_data[poll_answer.user.id][test_id]
                text = (f"⚜️Savollar: {test_uzunligi} ta "
                        f"\n\n❌ Xatolar: {xatolar} ta "
                        f"\n\n✅ To'g'ri javob: {test_uzunligi - xatolar} ta"
                        f"\n\n♻️Foizda: {100 - (xatolar * 100) / test_uzunligi}%")
                if len(xatolar_list) > 0:
                    tugma = InlineKeyboardMarkup(row_width=1)
                    tugma.add(InlineKeyboardButton(text="♻️ Xato testlar ustida ishlash", callback_data=f"Xato_testlar:"))
                    # tugma.add(InlineKeyboardButton(text="♻️ Qayta urinish", callback_data=f"qayta_urinish:{nom}:{db_test_id}:{test_uzunligi}:{uzunlik}"))
                    user_data[chat_id + 1] = [xatolar_list, nom, db_test_id]
                else:
                    tugma = None
                await bot.send_message(chat_id=chat_id, text=text, reply_markup=tugma)
        else:
            if current_question_index < uzunlik:
                await send_question(chat_id, test_id=test_id)
            else:
                xatolar_list = current_question['xatolar']
                nom = current_question['nom']
                db_test_id = current_question['db_test_id']
                text = (f"⚜️Savollar: {uzunlik} ta "
                        f"\n\n❌ Xatolar: {len(xatolar_list)} ta "
                        f"\n\n✅ To'g'ri javob: {uzunlik - len(xatolar_list)} ta"
                        f"\n\n♻️Foizda: {100 - (len(xatolar_list) * 100) / uzunlik}%")
                if len(xatolar_list) > 0:
                    tugma = InlineKeyboardMarkup(row_width=1)
                    tugma.add(InlineKeyboardButton(text="♻️ Xato testlar ustida ishlash", callback_data=f"Xato_testlar1:"))
                    tugma.add(InlineKeyboardButton(text="♻️ Qayta urinish",
                                                   callback_data=f"qayta_urinish1:{nom}:{db_test_id}:{uzunlik}:{uzunlik}"))
                    user_data[chat_id + 1] = [xatolar_list, nom, db_test_id]
                else:
                    tugma = None
                del user_data[poll_answer.user.id][test_id]
                await bot.send_message(chat_id=chat_id, text=text, reply_markup=tugma)
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0], text=f"process_poll 3: {e}")

@dp.callback_query_handler(lambda call: "Xato_testlar1:" in call.data)
async def xato_qayta_ishlash1(call: types.CallbackQuery):
    try:
        xatolar, nom, db_test_id = user_data[call.from_user.id + 1]
        user_data[call.from_user.id] = user_data.get(call.from_user.id, {})
        user_data[call.from_user.id][call.from_user.id] = {'raqam': 1, 'xatolar': [], 'test_turi': "random_test",
                                                           'db_test_id': int(db_test_id), 'nom': nom,
                                                           'sonlar': list(xatolar),
                                                           'test_uzunligi': len(list(xatolar))}
        await call.message.delete()
        await send_question(call.from_user.id)
    except Exception as e:
        await call.message.answer(text="xatolik yur berdi")
        await bot.send_message(chat_id=ADMINS[0], text=f"xato_qayta_ishlash {e}")



@dp.callback_query_handler(lambda call: "qayta_urinish1:" in call.data)
async def qayta_ishlash1(call: types.CallbackQuery):
    try:
        _, nom, db_test_id, test_uzunligi, uzunlik = call.data.split(":")
        user_data[call.from_user.id] = user_data.get(call.from_user.id, {})
        numbers = rn.sample(range(1, int(uzunlik) + 1), int(test_uzunligi))
        user_data[call.from_user.id][call.from_user.id] = {'raqam': 1, 'xatolar': [], 'db_test_id': int(db_test_id),
                                                           'nom': nom, 'test_turi':"random_test", 'sonlar': numbers}
        await send_question(tg_id=call.from_user.id)
    except Exception as e:
        await call.message.answer(text="xatolik yur berdi")
        await bot.send_message(chat_id=ADMINS[0], text=f"qayta_ishlash {e}")