import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatPermissions
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from dotenv import load_dotenv

# load_dotenv()

# Токен бота
API_TOKEN = os.getenv("BOT_TOKEN")

if not API_TOKEN:
    raise ValueError("BOT_TOKEN не задано! Перевір .env файл або змінні середовища.")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Обробка приєднання нового учасника
@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_member(message: types.Message):
    for member in message.new_chat_members:
        # Спочатку блокуємо нового користувача
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=member.id,
            permissions=ChatPermissions(can_send_messages=False)
        )

        # Кнопки для вибору
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            types.InlineKeyboardButton("Так, додайте мене хутчіш!", callback_data=f"rule_{member.id}_yes"),
            types.InlineKeyboardButton("Нєт", callback_data=f"rule_{member.id}_no")
        )

        # Повідомлення з правилами
        await message.reply(
            f"""👋 Привіт, {member.full_name}!

Це група 🇺🇦 Українців в Австрії, яких повʼязує інтерес до 🚴‍ велосипедів.

📌 *Спілкування у цій групі відбувається виключно українською мовою.*

Чи погоджуєшся ти із цим правилом і хочеш доєднатись?""",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

# Обробка відповіді на правила
@dp.callback_query_handler(lambda call: call.data.startswith("rule_"))
async def process_rule_answer(call: types.CallbackQuery):
    parts = call.data.split("_")
    user_id = int(parts[1])
    answer = parts[2]

    await call.answer()

    # Забороняємо іншим натискати кнопки
    if call.from_user.id != user_id:
        try:
            await call.answer("Це не твоє запитання.", show_alert=True)
        except Exception as e:
            print(f"Помилка при відправці alert: {e}")
        return

    await call.answer()

    if answer == "yes":
        # Дозволяємо користувачеві писати
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
        # Видаляємо користувача з групи
        await call.message.edit_text("Нажаль користувач не погодився із правилами. Доступ до групи заборонено.")
        await bot.kick_chat_member(chat_id=call.message.chat.id, user_id=user_id)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
