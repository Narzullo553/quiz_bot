from aiogram import types
from data.config import ADMINS
from filters import IsGroup, IsAdmin_group, IsAdmin_group_call
from loader import dp, db, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import asyncio
javoblar = {}
@dp.message_handler(IsGroup(), IsAdmin_group(), lambda message: '/start_tests_group' in message.text)
async def testlar_royhati(msg: types.Message):
    try:
        text, btn, db_id = await testlarim_xammasi12()
        await msg.reply(text=text, reply_markup=btn)
    except:
        await msg.reply(text=f"oltimos botni guruhga admin qiling")



async def testlarim_xammasi12(page=1, db_id=5):
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
                                                           callback_data=f"test123_group:{nomi['test_nomi']}:{nomi['telegram_id']}"))

            create_quiz_menu1.row(
                InlineKeyboardButton("◀", callback_data=f"page_group:{page-1}:{db_id}"),
                InlineKeyboardButton("❌", callback_data="cancel"),
                InlineKeyboardButton("▶", callback_data=f"page_group:{page+1}:{db_id}"),
            )
            return text, create_quiz_menu1,db_id
        else:
            return '', '', '',
    except:
        return


@dp.callback_query_handler(IsAdmin_group_call(), lambda call: "page_group:" in call.data)
async def testlar12(call: types.CallbackQuery):
    try:
        _, page, db_id = call.data.split(":")
        if int(page) > 0:
            if int(db_id) != 5:
                text,test, db_id = await testlarim_xammasi12(page=int(page))
            else:
                text, test, db_id = await testlarim_xammasi12(page=int(page), db_id=int(db_id))
            if test:
                await call.message.delete()
                await call.message.answer(text=f"📋 {text}", reply_markup=test)
            else:
                await call.answer("testlar topilmadi")
        else:
            await call.answer("testlar topilmadi")

    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0], text=f"test ro'yhati_group: {e}")

@dp.callback_query_handler(IsAdmin_group_call(),lambda call: "test123_group:" in call.data)
async def testni_boshlash_group(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    _, nom, db_id = call.data.split(":")
    await send_question(db_id=int(db_id), nom=nom, chat_id=chat_id)







async def send_question(db_id, nom, chat_id):
    try:
        data = await db.select_tests(telegram_id=db_id, test_nomi=nom)
        data = data[0]
        data = json.loads(data)

        for son, question in data.items():
            for text, question in question.items():
                try:
                    if question['#']:
                        javoblar1 = list(set(question['#']+question['+']))
                        msg = await bot.send_poll(
                            chat_id=chat_id,
                            question=text,
                            options=javoblar1,
                            type="quiz",
                            correct_option_id=javoblar1.index(question['#'][0]),
                            is_anonymous=False
                        )
                        javoblar[msg.poll.id] = [javoblar1.index(question['#'][0]), len(data), son, chat_id]
                        await asyncio.sleep(15)
                        try:
                            del javoblar[msg.poll.id]
                        except:
                            pass
                        await bot.stop_poll(chat_id=chat_id, message_id=msg.message_id)
                except Exception as e:
                    print(e)
        text = f"⚜️Savollar: {len(data)} ta"
        for user_id, javob in javoblar.items():
            member = await bot.get_chat_member(chat_id, user_id)
            text += f"\n{member.user.full_name}: {javob} ta"
            del javoblar[user_id]
        text += f"\nto'g'ri javob topishdi"
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0], text=f"send_questio {e}")


# @dp.poll_answer_handler()
async def process_poll_answer321(poll_answer: types.PollAnswer):
    try:
        user_id = poll_answer.user.id
        test_id = poll_answer.poll_id
        index, test_uzunligi, son, chat_id  = javoblar[test_id]
        if poll_answer.option_ids == [index]:
            xatolar = javoblar.get(user_id, {})
            if xatolar:
                javoblar[user_id] += 1
            else:
                javoblar[user_id] = 1
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0], text=f"process_poll11: {e}")
