from keyboards.menu import main_menu_kb
from aiogram import Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import json

router = Router()

class SearchStates(StatesGroup):
    waiting_for_keywords = State()

MESSAGES = {
    "English": {
        "ask": "🔍 Please enter keywords to search textbooks:",
        "not_found": "No results found for your query. Try other keywords.",
        "results": "📚 Search results:\n\n",
        "back_menu": "🔙 Returning to main menu.",
    },
    "Spanish": {
        "ask": "🔍 Introduce palabras clave para buscar libros de texto:",
        "not_found": "No se encontraron resultados para tu búsqueda. Prueba con otras palabras.",
        "results": "📚 Resultados de búsqueda:\n\n",
        "back_menu": "🔙 Volviendo al menú principal.",
    },
    "Portuguese": {
        "ask": "🔍 Insira palavras-chave para pesquisar livros didáticos:",
        "not_found": "Nenhum resultado encontrado para sua pesquisa. Tente outras palavras.",
        "results": "📚 Resultados da pesquisa:\n\n",
        "back_menu": "🔙 Retornando ao menu principal.",
    }
}

@router.message(lambda msg: msg.text in [
    "Search by Keywords",
    "Buscar por palabras clave",
    "Pesquisar por palavras-chave"
])
async def ask_keywords(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "English")
    await message.answer(MESSAGES.get(lang, MESSAGES["English"])["ask"])
    await state.set_state(SearchStates.waiting_for_keywords)

@router.message(SearchStates.waiting_for_keywords)
async def do_search(message: types.Message, state: FSMContext):
    query = message.text.lower()
    data = await state.get_data()
    lang = data.get("language", "English")

    try:
        with open("data/books.json", encoding="utf-8") as f:
            all_books = json.load(f)
    except Exception:
        await message.answer("Error loading textbooks.")
        return

    found = []
    for subject, books in all_books.items():
        for book in books:
            title = book["title"].get(lang, "")

            link = book["link"].get(lang) if isinstance(book["link"], dict) else book["link"]

            if query in title.lower():
                found.append((subject, title, link))

    if not found:
        await message.answer(MESSAGES.get(lang, MESSAGES["English"])["not_found"])
    else:
        reply = MESSAGES.get(lang, MESSAGES["English"])["results"]
        for subject, title, link in found:
            reply += f"• *{subject}* — [{title}]({link})\n"
        await message.answer(reply, parse_mode="Markdown", disable_web_page_preview=True)

    await message.answer(
        MESSAGES.get(lang, MESSAGES["English"])["back_menu"],
        reply_markup=main_menu_kb(lang)
    )
    await state.clear()
