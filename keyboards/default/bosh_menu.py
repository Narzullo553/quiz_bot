from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_menu.add(
    KeyboardButton("➕ Test yaratish"),
    KeyboardButton("📋 Testlarim"),
    KeyboardButton("🔍 Testlarni o‘rganish"),
    KeyboardButton("📊 Statistika"),
    KeyboardButton("📞 Qo'llab-quvvatlash"),
)
