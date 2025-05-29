from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def subject_kb(language: str) -> ReplyKeyboardMarkup:
    texts = {
        "English": ["Microeconomics", "Mathematics", "Main Menu"],
        "Spanish": ["Microeconomía", "Matemáticas", "Menú Principal"],
        "Portuguese": ["Microeconomia", "Matemática", "Menu Principal"],
    }

    subject_texts = texts.get(language, texts["English"])

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=subject_texts[0])],  # Microeconomics
            [KeyboardButton(text=subject_texts[1])],  # Mathematics
            [KeyboardButton(text=subject_texts[2])]   # Main Menu
        ],
        resize_keyboard=True
    )
    return keyboard
