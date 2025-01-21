from aiogram import types
import json
from docx import Document
import re
import io
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from docx.opc.oxml import nsmap

from data.config import ADMINS
from filters import IsPrivate
from loader import dp, db, bot
user_tests1 = {}


@dp.callback_query_handler(lambda call: "cancel" in call.data, state='')
async def cansel(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("jarayon yakunlandi")
    await call.message.delete()
    await state.finish()


@dp.message_handler(content_types=types.ContentType.DOCUMENT, state='file yubor')
async def faylni_qabul_qilish(msg: types.Message, state: FSMContext):
    document = msg.document
    name = document.file_name
    if name.endswith((".txt", ".docx")):
        file_buffer = io.BytesIO()
        await document.download(destination=file_buffer)
        file_buffer.seek(0)
        try:
            if name.endswith(".txt"):
                content = file_buffer.read().decode('utf-8')
            else:
                doc = Document(file_buffer)
                content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            data = await state.get_data()
            msge = data['msge']
            await msge.delete()
            await state.set_state('test_yoz1')
            await test_jonat(msg, content)
        except UnicodeDecodeError:
            await msg.reply("Fayl matn formatida emas yoki uni o'qib bo'lmadi.")
    else:
        await msg.answer("❌ Faqat .txt va .docx fayllarni qabul qilaman!")

@dp.message_handler(IsPrivate(), text="➕ Test yaratish")
async def test_yarat(msg: types.Message):
    try:
        tugma = InlineKeyboardMarkup(row_width=2)
        tugma.insert(InlineKeyboardButton(text="✍️ boshlash", callback_data=f"boshlash12"))
        tugma.insert(InlineKeyboardButton(text="📤 Fayl yuborish", callback_data=f"file"))
        await msg.answer("Yozishni boshlash uchun"
                         "\n✍️ boshlash bosing",
                         reply_markup=tugma)
    except:
        pass


@dp.callback_query_handler(lambda call: "file" in call.data)
async def test_yarat_b(call: types.CallbackQuery, state: FSMContext):
    user_tests1[call.from_user.id] = {}
    tugma = InlineKeyboardMarkup(row_width=2)
    tugma.insert(InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"cancel"))
    text = ("Test fileni yuborishingiz mumkin"
            "Iltimos, test savol va javoblaringizni quyidagicha yuboring:\n\n"
            "1. [Savolingiz] \nJavoblar: \n=====\n[Javob 1],\n=====\n# [To‘g‘ri javob],\n=====\n[Javob 2], \n++++\n...\n"
            "Masalan: 1. Bu qanday savol? \n=====\n Boshqa tizim,\n=====\n#Testni ishlatish,\n=====\nYangi metod!")
    await call.message.delete()
    await state.set_state('file yubor')
    msg = await call.message.answer(text, reply_markup=tugma)
    await state.update_data({'msge': msg})



@dp.callback_query_handler(lambda call: "boshlash12" in call.data)
async def test_yarat_b(call: types.CallbackQuery, state: FSMContext):
    try:
        user_tests1[call.from_user.id] = {}
        tugma = InlineKeyboardMarkup(row_width=2)
        tugma.insert(InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"cancel"))
        await call.message.delete()
        await state.set_state("test_yoz")
        await call.message.answer("Iltimos, test savol va javoblaringizni quyidagicha yuboring:\n\n"
                             "1. [Savolingiz] \nJavoblar: \n=====\n[Javob 1],\n=====\n# [To‘g‘ri javob],\n=====\n[Javob 2], \n++++\n...\n"
                             "Masalan: 1. Bu qanday savol? \n=====\n Boshqa tizim,\n=====\n#Testni ishlatish,\n=====\nYangi metod!"
                                  "\ntestlarni 10 ta qilib bo'lib bo'lib yuboring",
                         reply_markup=tugma)
    except:
        pass

@dp.callback_query_handler(text="save_and_finish", state="test_yoz")
async def test_saqlash(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="test uchun nom bering")
    await call.message.delete()
    await state.set_state("saqlash")

@dp.callback_query_handler(text="save_and_finish", state="test_yoz1")
async def test_saqlash1(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text="test uchun nom bering")
    await call.message.delete()
    await state.set_state("saqlash")

@dp.message_handler(state="saqlash")
async def saqlash(msg: types.Message, state: FSMContext):
    try:
        user_tests = user_tests1[msg.from_user.id]
        json_data = json.dumps(user_tests, ensure_ascii=False)
        del user_tests1[msg.from_user.id]
        await db.add_savollar(telegram_id=msg.from_user.id, test_nomi=msg.text, test=json_data)
        await msg.answer("test saqlandi")
        await state.finish()
    except:
        pass



@dp.callback_query_handler(text="cancel", state="test_yoz")
async def test_saqlash(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("yakunlandi")
    await call.message.delete()
    await state.finish()


# @dp.message_handler(IsPrivate(), state="test_yoz")
# async def test_jonat(msg: types.Message, state: FSMContext):
    # user_tests = {}
    # input_text = msg.text
    # questions = re.split(r'\d+\.', input_text)
    # questions = [q.strip() for q in questions if q.strip()]
    # print(questions)
#     for i, q in enumerate(questions, start=1):
#         lines = q.split('\n')
#         question_text = lines[0].strip()
#         answers = {'+': [], '#': []}
#         for line in lines[1:]:
#             line = line.strip()
#             if line.startswith('+'):  # To'g'ri javob
#                 answers['+'].append(line[1:].strip())
#             elif line.startswith('#'):  # Notog'ri javob
#                 answers['#'].append(line[1:].strip())
#         unique_key = f"{question_text}"
#         user_tests[i] = {unique_key:answers}
#     tugma = InlineKeyboardMarkup(row_width=2)
#     tugma.insert(InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"cancel"))
#     tugma.insert(InlineKeyboardButton(text="💾 Saqlash va tugatish", callback_data=f"save_and_finish"))
#     user_tests1[msg.from_user.id].update(user_tests)
#     await msg.answer(text="Davom etishingiz mumkin"
#                           "\nagar saqlamoqchi yoki to'xtatmoqchi bo'lsangiz"
#                           "\nmos tugmani bosing", reply_markup=tugma)


async def is_quiz_format_valid(input_string):
    pattern = r"""
    ^\d+\."
    """
    return bool(re.match(pattern, input_string, re.MULTILINE | re.VERBOSE))


async def test_jonat(msg, texti):
    try:
        user_tests = {}
        input_text = texti
        a = await is_quiz_format_valid(input_text)
        if a:
            questions = re.split(r'\d+\.', input_text)
        else:
            questions = re.split(r'\++', input_text)
        questions = [q.strip() for q in questions if q.strip()]
        x = 1
        for i, q in enumerate(questions, start=1):
            while '=' in q:
                q = q.replace('=', '')
            while '+' in q:
                q = q.replace('+', '')
            lines = q.split('\n')
            question_text = lines[0].strip()
            answers = {'+': [], '#': []}
            for line in lines[1:]:
                line = line.strip()
                if line:
                    if line[0] == '#':
                        answers['#'].append(line[1:])
                    else:
                        answers['+'].append(line)
            if answers['#']:
                unique_key = f"{question_text}"
                user_tests[x] = {unique_key:answers}
                x += 1
        tugma = InlineKeyboardMarkup(row_width=2)
        tugma.insert(InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"cancel"))
        tugma.insert(InlineKeyboardButton(text="💾 Saqlash va tugatish", callback_data=f"save_and_finish"))
        user_tests1[msg.from_user.id].update(user_tests)
        await msg.answer(text="Davom etishingiz mumkin"
                              "\nagar saqlamoqchi yoki to'xtatmoqchi bo'lsangiz"
                              "\nmos tugmani bosing", reply_markup=tugma)
    except Exception as e:
        await bot.send_message(chat_id=ADMINS[0], text=e)

@dp.message_handler(IsPrivate(), state="test_yoz")
async def test_jonatish(msg: types.Message):
    await test_jonat(msg=msg, texti=msg.text)



test = """1. savol?
====
variant
====
variant
====
# to'g'ri javob
====
variant
++++
2. savol?
"""