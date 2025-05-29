from aiogram import Router, types
from aiogram.filters import Command

router = Router()

help_texts = {
    "English": "https://drive.google.com/file/d/1oAOHR83fFAJDr1uAmhLuC_ONAAJz5wxI/view",
    "Spanish": "https://drive.google.com/file/d/1oAOHR83fFAJDr1uAmhLuC_ONAAJz5wxI/view",
    "Portuguese": "https://drive.google.com/file/d/1oAOHR83fFAJDr1uAmhLuC_ONAAJz5wxI/view"
}

@router.message(Command("help"))
async def help_handler(message: types.Message, state):
    data = await state.get_data()
    lang = data.get("language", "English")
    await message.answer(help_texts.get(lang, help_texts["English"]))

@router.message(lambda msg: msg.text in ["Help", "Ayuda", "Ajuda"])
async def help_button_handler(message: types.Message, state):
    data = await state.get_data()
    lang = data.get("language", "English")
    await message.answer(help_texts.get(lang, help_texts["English"]))
