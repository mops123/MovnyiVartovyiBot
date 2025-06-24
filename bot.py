import os
import asyncio
from aiohttp import web
from dotenv import load_dotenv

# === Базовий HTTP сервер для Render ===
async def handle(request):
    return web.Response(text="✅ I'm alive!")

async def run_webserver():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.environ.get("PORT", 8080))  # обов'язково для Render
    site = web.TCPSite(runner, "0.0.0.0", port=port)
    await site.start()
    print(f"🌐 Web server is running on port {port}")

# === Telegram Bot ===
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatPermissions
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
if not API_TOKEN:
    raise ValueError("BOT_TOKEN не задано! Перевір .env файл або змінні середовища.")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_member(message: types.Message):
    chat = await bot.get_chat(message.chat.id)
    group_name = chat.title or "ця група"
    group_description = chat.description or ""

    for member in message.new_chat_members:
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=member.id,
            permissions=ChatPermissions(can_send_messages=False)
        )

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            types.InlineKeyboardButton("Так, додайте мене хутчіш!", callback_data=f"rule_{member.id}_yes"),
            types.InlineKeyboardButton("Нєт", callback_data=f"rule_{member.id}_no")
        )

        message_text = f"""👋 Привіт, {member.full_name}!

Це група {group_name}{f". {group_description}" if group_description else ""}

📌 Спілкування у цій групі відбувається виключно Українською мовою.

Чи погоджуєшся ти із цим правилом і хочеш доєднатись?
"""

        await message.reply(message_text, reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data.startswith("rule_"))
async def process_rule_answer(call: types.CallbackQuery):
    parts = call.data.split("_")
    user_id = int(parts[1])
    answer = parts[2]

    await call.answer()

    if call.from_user.id != user_id:
        try:
            await call.answer("Це не твоє запитання.", show_alert=True)
        except Exception as e:
            print(f"Помилка при відправці alert: {e}")
        return

    if answer == "yes":
        await bot.restrict_chat_member(
            chat_id=call.message.chat.id,
            user_id=user_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await call.message.edit_text("✅ Вітаю! Тепер ти можеш писати у групі. Ласкаво просимо!")
    else:
        await call.message.edit_text("Нажаль користувач не погодився із правилами. Доступ до групи заборонено.")
        await bot.kick_chat_member(chat_id=call.message.chat.id, user_id=user_id)

# === Запуск бота + вебсервер одночасно ===
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_webserver())             # 🧠 HTTP keepalive
    executor.start_polling(dp, skip_updates=True) # 🤖 Telegram бот
