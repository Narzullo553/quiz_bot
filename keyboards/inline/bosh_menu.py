from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

create_quiz_menu = InlineKeyboardMarkup(row_width=1)
create_quiz_menu.add(
    InlineKeyboardButton("✍️ Savol qo'shish", callback_data="add_question"),
    InlineKeyboardButton("✅ To‘g‘ri javob tanlash", callback_data="select_answer"),
    InlineKeyboardButton("💾 Saqlash va tugatish", callback_data="save_and_finish"),
)

support_menu = InlineKeyboardMarkup(row_width=1)
support_menu.add(
    InlineKeyboardButton("📞 Aloqa", url="https://t.me/support_username"),
    InlineKeyboardButton("💡 Fikr qoldirish", callback_data="feedback"),
    InlineKeyboardButton("❓ Yordam", callback_data="help"),
)
