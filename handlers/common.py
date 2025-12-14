from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from db.session import add_user, reset_context



router = Router()

# buttons
btn_reply = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Новый запрос")]], resize_keyboard=True)
btn_inline = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Новый запрос", callback_data="new_request")]])


# /start and reset
@router.message(Command("start"))
async def cmd_start(message: Message):
    print(f"[cmd_start] {message.from_user.username} ({message.from_user.id}): {message.text}")

    add_user(message.from_user.id)
    reset_context(message.from_user.id)

    await message.answer("Начат новый диалог", reply_markup=btn_reply)


@router.message(Command("help"))
async def cmd_help(message: Message):
    print(f"[cmd_help] {message.from_user.username} ({message.from_user.id}): {message.text}")

    await message.answer(
        "Команды:\n"
        "/start — начать новый диалог\n"
        "/help — справка\n"
        "Кнопки 'Новый запрос' — начинают новый диалог"
    )

# REPLY
@router.message(lambda m: m.text == "Новый запрос")
async def new_request_reply(message: Message):
    print(f"[new_request_reply] {message.from_user.username} ({message.from_user.id}): {message.text}")

    reset_context(message.from_user.id)
    await message.answer("Начат новый диалог", reply_markup=btn_inline)

# INLINE
@router.callback_query(lambda c: c.data == "new_request")
async def new_request_inline(callback_query: CallbackQuery):
    user = callback_query.from_user
    print(f"[new_request_inline] {user.username} ({user.id}) 'Новый запрос'")

    reset_context(user.id)
    await callback_query.message.answer("Начат новый диалог", reply_markup=btn_reply)

