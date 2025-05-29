from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

language_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="English")],
        [KeyboardButton(text="Spanish")],
        [KeyboardButton(text="Portuguese")]
    ],
    resize_keyboard=True
)
