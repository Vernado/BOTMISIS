from aiogram import Router, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from keyboards.language import language_kb
from keyboards.menu import main_menu_kb

router = Router()

class Form(StatesGroup):
    language = State()
    subject = State()

@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await message.answer("Hi! Please choose a language:", reply_markup=language_kb)
    await state.set_state(Form.language)

@router.message(Form.language)
async def language_chosen(message: Message, state: FSMContext):
    lang = message.text
    await state.update_data(language=lang)

    if lang == "English":
        text = "Now choose a subject:"
    elif lang == "Spanish":
        text = "Ahora elige una materia:"
    elif lang == "Portuguese":
        text = "Agora escolha uma matéria:"
    else:
        text = "Now choose a subject:" 

    main_menu = main_menu_kb(lang)
    await message.answer(text, reply_markup=main_menu)
    await state.set_state(Form.subject)
