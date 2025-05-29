from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import ADMIN_ID

router = Router()

class FeedbackState(StatesGroup):
    waiting_for_feedback = State()
    waiting_for_admin_reply = State()

feedback_texts = {
    "English": {
        "request": "✉️ Please write your message, and I will forward it to the administrator:",
        "sent": "✅ Message sent. The administrator will reply soon.",
        "admin_reply": "💬 Administrator's reply:\n\n"
    },
    "Spanish": {
        "request": "✉️ Por favor escribe tu mensaje y se lo enviaré al administrador:",
        "sent": "✅ Mensaje enviado. El administrador responderá pronto.",
        "admin_reply": "💬 Respuesta del administrador:\n\n"
    },
    "Portuguese": {
        "request": "✉️ Por favor escreva sua mensagem e eu a encaminharei ao administrador:",
        "sent": "✅ Mensagem enviada. O administrador responderá em breve.",
        "admin_reply": "💬 Resposta do administrador:\n\n"
    }
}

user_feedback_map = {}

@router.message(Command("feedback"))
@router.message(lambda msg: msg.text in ["Feedback", "Retroalimentación", "Feedback"])
async def request_feedback(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("language", "English")
    await message.answer(feedback_texts.get(lang, feedback_texts["English"])["request"])
    await state.set_state(FeedbackState.waiting_for_feedback)

@router.message(FeedbackState.waiting_for_feedback)
async def forward_feedback(message: types.Message, state: FSMContext):
    user = message.from_user
    text = message.text
    data = await state.get_data()
    lang = data.get("language", "English")

    feedback_text = f"📩 New message from @{user.username or 'no username'} (ID: {user.id}):\n\n{text}"

    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✉️ Reply to user", callback_data=f"reply_to:{user.id}")
    ]])

    sent = await message.bot.send_message(ADMIN_ID, feedback_text, reply_markup=keyboard)

    user_feedback_map[sent.message_id] = user.id

    await message.answer(feedback_texts.get(lang, feedback_texts["English"])["sent"])
    await state.clear()

@router.callback_query(F.data.startswith("reply_to:"))
async def handle_reply_button(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split(":")[1])
    await state.set_state(FeedbackState.waiting_for_admin_reply)
    await state.update_data(reply_to_user_id=user_id)

    await callback.message.answer(f"✍️ Please type your reply to the user (ID: {user_id}):")
    await callback.answer()

@router.message(FeedbackState.waiting_for_admin_reply, F.chat.id == ADMIN_ID)
async def send_admin_reply(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("reply_to_user_id")

    if user_id:
        lang = "English"
        await message.bot.send_message(user_id, f"{feedback_texts[lang]['admin_reply']}{message.text}")
        await message.answer("✅ Reply sent to user.")
    else:
        await message.answer("⚠️ Could not find user to reply.")

    await state.clear()
