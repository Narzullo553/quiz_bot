from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

zamdekan_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
zamdekan_menu.add(
    KeyboardButton("📚 Darslar nazorati"),
    KeyboardButton("📇 Xodimlar Kontaktlari"),
    KeyboardButton("📢 Eslatmalar va E'lonlar"),
    KeyboardButton("📥 Yangi Murojaatlar"),
    KeyboardButton("⚙️ Bot Sozlamalari")
)
