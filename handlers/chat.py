from aiogram import Router
from aiogram.types import Message
from openai import OpenAI
from db.session import add_user, save_message, get_context
from core.config import OPENAI_API_KEY
from handlers.common import btn_reply, btn_inline
import traceback


router = Router()
client = OpenAI(api_key=OPENAI_API_KEY)

# HARDCODE SECTION
user_requests = {}
FREE_USAGE_LIMIT = 25


@router.message()
async def message_handler(message: Message):
    user_id = message.from_user.id
    print("-" * 18)
    print(f"[USER] {message.from_user.username} ({user_id}): {message.text}")

    add_user(user_id)

    count = user_requests.get(user_id, 0) + 1
    user_requests[user_id] = count

    if count > FREE_USAGE_LIMIT:
        await message.answer("Засылайте $ или разговор закончен.", reply_markup=btn_reply)
        print(f"[COUNT] Спёкся, голубок: {message.from_user.username} ({user_id}). Iters: ({count})")
        return

    save_message(user_id, "user", message.text)
    context = get_context(user_id, limit=10)


    system_prompt = {
        "role": "system",
        "content": "Ты — обычный GPT‑ассистент. \
            Тебе будут приходить сообщения пользователя и контекст диалога, если он есть.\
            Используй этот контекст для связных ответов, но если контекста нет — отвечай как обычно.\
            Отвечай понятно, по делу и в дружелюбном стиле."
    }

    messages = [system_prompt] + context

    print("*" * 10)
    print(f"messages context: {messages}")
    print("*" * 10)

    try:
        completion = client.chat.completions.create(
            model="gpt-5-nano",
            messages=messages
        )
        answer = completion.choices[0].message.content
        print(f"[BOT] {message.from_user.username} ({user_id}): {answer}")
        save_message(user_id, "assistant", answer)

    except Exception:
        answer = "Ошибка при обращении к OpenAI API."
        print(f"[message_handler][ERROR] request error: {traceback.format_exc()}")

    await message.answer(answer, reply_markup=btn_inline)

    print(f"count: {count}")
