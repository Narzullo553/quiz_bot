from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bosh_menu =ReplyKeyboardMarkup(
    row_width=2,resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="📰 Yangiliklar"),
            KeyboardButton(text="📚 Dars Jadvali")
        ],
        [
            KeyboardButton(text="✉️Murojaat"),
            KeyboardButton(text="📞 Kontaktlar")
        ],
        [
            KeyboardButton(text="❓ Tez-tez So'raladigan Savollar")
        ]
    ]
)
