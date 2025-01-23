import asyncio
import re
import random as rn

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiohttp.web_routedef import delete

from data.config import ADMINS
from filters import IsPrivate, IsPrivateChatFilter
from handlers.groups.testlar_royhati_groups import process_poll_answer321, javoblar
from handlers.users.timersiz import  process_poll_answer1, clear
from loader import dp, db, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
user_data = {}
active_polls = {}

@dp.message_handler(text="ochir")
async def Clear(msg: types.Message):
    await clear()
    global user_data, active_polls
    user_data = {}
    active_polls = {}


@dp.message_handler(IsPrivate(),text="📋 Testlarim")
async def testlar(msg: types.Message):
    try:
        text, test, db_id = await testlarim_xammasi1(db_id=msg.from_user.id)
        if test==2:
            await msg.answer(text=f"📋 sizda hozirda testlar mavjud emas")
        else:
            await msg.answer(text=f"📋 {text}", reply_markup=test)
    except:
        await msg.answer(text=f"📋 sizda hozirda testlar mavjud emas")



async def testlarim_xammasi1(db_id, page=1):
    try:
        uzunlik = await db.test_count1(int(db_id))
        if uzunlik+10 - page*10 >=0:
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
                InlineKeyboardButton("◀", callback_data=f"page1:{page-1}:{db_id}"),
                InlineKeyboardButton("❌", callback_data="cancel"),
                InlineKeyboardButton("▶", callback_data=f"page1:{page+1}:{db_id}"),
            )
            return text, create_quiz_menu1, db_id
        else:
            return 2, 2, 2
    except:
        return


@dp.callback_query_handler(lambda call: "page1:" in call.data)
async def testlar12(call: types.CallbackQuery):
    try:
        _, page, db_id = call.data.split(":")
        if int(page) > 0:
            text, test, db_id = await testlarim_xammasi1(db_id=call.from_user.id)
            if test:
                await call.message.delete()
                await call.message.answer(text=f"📋 {text}", reply_markup=test)
            else:
                await call.answer("testlar topilmadi")
        else:
            await call.answer("testlar topilmadi")
    except:
        await call.answer("testlar topilmadi")





@dp.callback_query_handler(lambda call: "ochir:" in call.data)
async def ochir(call: types.CallbackQuery):
    try:
        _, nom, db_id = call.data.split(":")
        await db.delete_tests(int(db_id), nom)
        await call.message.delete()
        await call.message.answer("test o'chirildi")
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0], text=f"ochir {e}")

"""testni boshlash qismi"""
async def testni_boshlash1(call, tg_id=None, nom=None):
    try:
        if tg_id is None:
            tg_id = call.from_user.id
            nom = call.data.replace('boshlash_1:', '')
        minutlar = [10, 15, 20, 30]
        tugma = InlineKeyboardMarkup(row_width=2)
        for i in minutlar:
            tugma.insert(InlineKeyboardButton(text=f"⏲️ - {i}", callback_data=f"soniya:{i}:{nom}:{tg_id}"))
        tugma.add(InlineKeyboardButton(text=f"⏲️ - Timersiz", callback_data=f"soniyasiz:{nom}:{tg_id}"))
        text = (f"test: {nom}"
                f"necha soniyada almashsin"
                f"tugmalardan birini tanlang")
        await call.message.answer(text=text, reply_markup=tugma)
    except:
        await call.message.answer("xatolik yuz berdi")
        return

@dp.callback_query_handler(lambda call: "soniya:" in call.data)
async def Soniya(call: types.CallbackQuery):
    try:
        _,soniya, nom, db_id = call.data.split(":")
        await testni_boshlash123(call,soniya, nom, db_id)
    except:
        await call.message.answer("xatolik yuz berdi")
        return


async def testni_boshlash123(call,soniya, nom, tg_id):
    try:
        await call.message.delete()
        tugma = InlineKeyboardMarkup(row_width=1)
        tugma.add(InlineKeyboardButton(text="🔀 - Tasodifiy Test:", callback_data=f"random_test:{soniya}:{nom}:{tg_id}"))
        tugma.add(InlineKeyboardButton(text="✅ - Oddiy Test:", callback_data=f"oddiy_test:{soniya}:{nom}:{tg_id}"))
        await bot.send_message(chat_id=call.from_user.id,
                               text="Test qay tarzda o'tkazilsin", reply_markup=tugma)
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0], text=f"testni_boshlash1 {e}")


@dp.callback_query_handler(lambda call: "oddiy_test" in call.data)
async def oddiy_test(call: types.CallbackQuery):
    try:
        await call.message.delete()
        _,soniya, nom, tg_id = call.data.split(":")
        await send_quiz(chat_id=call.from_user.id, db_id=int(tg_id),soniya=soniya, db_name=nom, question_index=1)
    except:
        await call.message.answer("hatolik yuz berdi")

@dp.callback_query_handler(lambda call: "random_test" in call.data)
async def random_test(call: types.CallbackQuery, state: FSMContext):
    try:
        _,soniya, nom, tg_id = call.data.split(":")
        data = await db.select_tests(telegram_id=int(tg_id), test_nomi=nom)
        data = data[0]
        data = json.loads(data)
        text = ("test miqdori kiriting !!"
                f"\n{len(data)} dan kam miqdor kiriting"
                f"\nmisol: 20 ta"
                f"\n/cancel bekor qilish")
        await call.message.delete()
        await call.message.answer(text=text)
        await state.set_state('test_soni_yubor')
        await state.update_data({'uzumlik': len(data), 'nom': nom, 'db_id':tg_id,'soniya': soniya})
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0], text=f"randomtest: {e}")

@dp.message_handler(state='test_soni_yubor')
async def test_soni(msg: types.Message, state: FSMContext):
    try:
        number = re.findall(r'\d+', msg.text)
        datas = await state.get_data()
        l = datas['uzumlik']
        nom = datas['nom']
        db_id = datas['db_id']
        soniya = datas['soniya']
        if int(number[0]) > l:
            await msg.answer(f"iltimos {l} dan kam miqdor kiriting")
        else:
            numbers = rn.sample(range(1, l+1), int(number[0]))
            await state.finish()
            await send_quiz(chat_id=msg.from_user.id, db_name=nom, db_id=int(db_id), sonlar=numbers, soniya=soniya, uzunlik=int(number[0]))
    except:
        await msg.answer(f"iltimos test miqdorini to'g'ri kiriting")



@dp.callback_query_handler(lambda call: "boshlash_1:" in call.data)
async def testni_boshlash12(call: types.CallbackQuery):
    await call.message.delete()
    _,nom, db_id = call.data.split(":")
    await testni_boshlash1(call, tg_id=int(db_id), nom=nom)




user_answers = {}

async def send_quiz(chat_id, db_name, db_id, soniya, question_index=0,uzunlik=0, sonlar=None, s = 1):
    try:
        """Viktorinani jo'natish va boshqarish."""

        data = await db.select_tests(telegram_id=db_id, test_nomi=db_name)
        data = data[0]
        data = json.loads(data)
        if question_index:
            savol = question_index
        else:
            if sonlar:
                savol = sonlar.pop(0)
            else:
                del user_answers[chat_id]
                del active_polls[chat_id]
                text, tugma = await restart(user_id=chat_id)
                await bot.send_message(chat_id,text=text, reply_markup=tugma)
                return
        if savol >= len(data):
            del user_answers[chat_id]
            del active_polls[chat_id]
            await bot.send_message(chat_id, "Viktorina tugadi! Rahmat ishtirok etganingiz uchun.")
            return
        questions = data[f'{savol}']
        javob_idex = 0
        # Viktorinani jo'natish
        javoblar_x = []
        for text, question in questions.items():
            if text:
                javoblar = list(set(question['#']+question['+']))
                javoblar_x = javoblar

                try:
                    msg = await bot.send_poll(
                                chat_id=chat_id,
                                question=text,
                                options=javoblar,
                                type="quiz",
                                correct_option_id=javoblar.index(question['#'][0]),
                                is_anonymous=False
                            )
                    javob_idex = javoblar.index(question['#'][0])
                    active_polls[chat_id] = msg.message_id
                except Exception as e:
                    print('a', e)
            else:
                if question_index:
                    await send_quiz(chat_id=chat_id, db_name=db_name, db_id=db_id, soniya=soniya, question_index=savol + 1,
                                    uzunlik=len(data), s=s + 1)
                else:
                    await send_quiz(chat_id=chat_id, db_name=db_name, db_id=db_id, soniya=soniya, sonlar=sonlar+[savol+1],
                                    uzunlik=uzunlik, s= s + 1)
                return

        # 15 soniya kutish
        await asyncio.sleep(int(soniya))
        await bot.stop_poll(chat_id=chat_id, message_id=msg.message_id)
        # Foydalanuvchi to'g'ri javob berganini tekshirish
        if chat_id in user_answers and msg.poll.id in user_answers[chat_id]:
            user_answer = user_answers[chat_id][msg.poll.id]
            del user_answers[chat_id][msg.poll.id]
            if user_answer != [javob_idex]:
                user_answers[chat_id]['xatolar'].append(savol)
        else:
            if chat_id not in user_answers:
                user_answers[chat_id] = {'xatolar': []}
            user_answers[chat_id]['xatolar'].append(savol)
        xatolar = user_answers[chat_id]['xatolar']
        user_data[chat_id + 1] = {
            'db_name': db_name,
            'db_id': db_id,
            'soniya': soniya,
            'xatolar': xatolar,
            'test_uzunligi': len(data),
            'uzunlik': uzunlik,
            'son': s
        }
        if question_index:
            await send_quiz(chat_id = chat_id,db_name= db_name, db_id=db_id,soniya=soniya, question_index=savol + 1, uzunlik=len(data), s = s + 1)
        else:
            await send_quiz(chat_id=chat_id,db_name= db_name,db_id= db_id,soniya=soniya, sonlar=sonlar, uzunlik=uzunlik, s = s + 1)


    except Exception as e:
        pass



@dp.poll_answer_handler(IsPrivate())
async def process_poll_answer(poll_answer: types.PollAnswer):
    try:
        chat_id = poll_answer.user.id
        test_id = poll_answer.poll_id
        if chat_id in active_polls:
            answer_idex = poll_answer.option_ids
            if chat_id not in user_answers:
                user_answers[chat_id] = {'xatolar': []}
            user_answers[chat_id][test_id] = answer_idex
        elif test_id in javoblar:
            await process_poll_answer321(poll_answer)
        else:
            await process_poll_answer1(poll_answer)
    except:
        print('e')


async def restart(user_id=None, a = 0):
    try:
        datas = user_data[user_id + 1]
        xatolar1 = len(datas['xatolar'])
        test_uzunligi = datas['test_uzunligi']
        uzunlik = datas['uzunlik']
        son = datas['son']
        if uzunlik:
            test_uzunligi = uzunlik
        text = (f"⚜️Savollar: {test_uzunligi} ta "
                f"\n\n❌ Xatolar: {xatolar1+a} ta "
                f"\n\n✅ To'g'ri javob: {son - xatolar1} ta"
                f"\n\n♻️Foizda: {100 - ((xatolar1+a) * 100) / test_uzunligi}%")
        tugma = InlineKeyboardMarkup(row_width=1)
        tugma.add(InlineKeyboardButton(text="♻️ Xato testlar ustida ishlash", callback_data=f"Xato_testlar:"))
        # tugma.add(InlineKeyboardButton(text="♻️ Qayta urinish", callback_data=f"qayta_urinish:{nom}:{db_test_id}:{test_uzunligi}:{uzunlik}:{soniya}"))
        return text, tugma
    except:
        text, tugma = "❌ Xatolar: 0 ta ", None






@dp.callback_query_handler(lambda call: "Xato_testlar:" in call.data)
async def qayta_ishlash(call: types.CallbackQuery):
    try:
        datas = user_data[call.from_user.id + 1]
        del user_data[call.from_user.id + 1]
        db_id = datas['db_id']
        db_name = datas['db_name']
        soniya = datas['soniya']
        xatolar = datas['xatolar']
        await send_quiz(chat_id=call.from_user.id, db_name=db_name,
                        db_id=db_id, soniya=soniya, sonlar=xatolar)
    except Exception as e:
        await call.message.answer(text="xatolik yur berdi")
        await bot.send_message(chat_id=ADMINS[0], text=f"qayta_ishlash {e}")


@dp.message_handler(IsPrivate(), commands=['stop'])
async def bot_start(message: types.Message):
    try:
        if message.from_user.id in active_polls:
            m_id = active_polls[message.from_user.id]
            await bot.stop_poll(chat_id=message.from_user.id,message_id=m_id)
            text, tugma = await restart(user_id=message.from_user.id, a=1)
            await message.answer(text=text, reply_markup=tugma)
            try:
                del active_polls[message.from_user.id]
                del user_answers[message.from_user.id]
            except Exception as e:
                print('sd', e)
        else:
            await message.answer("sizda hali test yo")
    except Exception as err:
        print('e',err)