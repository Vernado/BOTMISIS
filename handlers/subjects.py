from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from .start import Form
from keyboards.subjects import subject_kb
from keyboards.menu import main_menu_kb
import json

router = Router()

@router.message(lambda msg: msg.text in [
    "Choose Subject", "Elegir materia", "Escolher matéria"
])
async def choose_subject(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "English")
    keyboard = subject_kb(lang)

    texts = {
        "English": "Choose a subject:",
        "Spanish": "Ahora elige una materia:",
        "Portuguese": "Agora escolha uma matéria:"
    }
    text = texts.get(lang, "Choose a subject:")

    await message.answer(text, reply_markup=keyboard)
    await state.set_state(Form.subject)

@router.message(Form.subject)
async def show_books(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "English")

    subjects_map = {
        "English": ["Microeconomics", "Mathematics", "Theoretical Economics", "Economics and Finance of Organizations"],
        "Spanish": ["Microeconomía", "Matemáticas", "Economía Teórica", "Economía y Finanzas de Organizaciones"],
        "Portuguese": ["Microeconomia", "Matemática", "Economia Teórica", "Economia e Finanças das Organizações"]
    }

    back_texts = {
        "English": "Main Menu",
        "Spanish": "Menú Principal",
        "Portuguese": "Menu Principal"
    }

    if message.text == back_texts.get(lang):
        keyboard = main_menu_kb(lang)
        reply_texts = {
            "English": "Main menu:",
            "Spanish": "Menú principal:",
            "Portuguese": "Menu principal:"
        }
        await message.answer(reply_texts.get(lang, "Main menu:"), reply_markup=keyboard)
        await state.set_state(Form.subject) 
        return

    
    subject_internal = None
    for internal, names in zip(subjects_map["English"], zip(*[subjects_map[l] for l in subjects_map])):
        if message.text in names:
            subject_internal = internal
            break

    if not subject_internal:
        await message.answer({
            "English": "Please choose a subject from the menu.",
            "Spanish": "Por favor, elige una materia del menú.",
            "Portuguese": "Por favor, escolha uma matéria do menu."
        }.get(lang, "Please choose a subject from the menu."))
        return

    try:
        with open("data/books.json", encoding="utf-8") as f:
            books = json.load(f).get(subject_internal, [])
    except Exception:
        await message.answer({
            "English": "Failed to load textbooks.",
            "Spanish": "No se pudieron cargar los libros de texto.",
            "Portuguese": "Falha ao carregar os livros didáticos."
        }.get(lang, "Failed to load textbooks."))
        return

    if not books:
        await message.answer({
            "English": "No textbooks found.",
            "Spanish": "No se encontraron libros de texto.",
            "Portuguese": "Nenhum livro didático encontrado."
        }.get(lang, "No textbooks found."))
        return

    reply = f"📚 Textbooks for *{message.text}*:\n\n"
    for book in books:
        title = book["title"].get(lang, next(iter(book["title"].values())))
        
        link = book["link"].get(lang) if isinstance(book["link"], dict) else book["link"]

        reply += f"• [{title}]({link})\n"

    await message.answer(reply, parse_mode="Markdown", disable_web_page_preview=True)
