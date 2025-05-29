from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_kb(language: str) -> ReplyKeyboardMarkup:
    texts = {
        "English": {
            "choose_subject": "Choose Subject",
            "search_keywords": "Search by Keywords",
            "help": "Help",
            "feedback": "Feedback"
        },
        "Spanish": {
            "choose_subject": "Elegir materia",
            "search_keywords": "Buscar por palabras clave",
            "help": "Ayuda",
            "feedback": "Retroalimentación"
        },
        "Portuguese": {
            "choose_subject": "Escolher matéria",
            "search_keywords": "Pesquisar por palavras-chave",
            "help": "Ajuda",
            "feedback": "Comentários"
        }
    }

    lang_texts = texts.get(language, texts["English"])

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=lang_texts["choose_subject"])],
            [KeyboardButton(text=lang_texts["search_keywords"])],
            [KeyboardButton(text=lang_texts["help"]), KeyboardButton(text=lang_texts["feedback"])]
        ],
        resize_keyboard=True
    )
    return keyboard
