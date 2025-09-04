from aiogram import types, Dispatcher
from aiogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from app.bot import bot  # використовується в хендлерах

def register_handlers(dp: Dispatcher):
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

            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(
                InlineKeyboardButton("Нєт", callback_data=f"rule_{member.id}_no"),
                InlineKeyboardButton("Так, додайте мене хутчіш!", callback_data=f"rule_{member.id}_yes")
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
            await call.answer("Це не твоє запитання.", show_alert=True)
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
            await call.message.edit_text("Ласкаво просимо! Тепер ти можеш писати у групі.\n\nНапиши кілька слів про себе! 🙂")
        else:
            await call.message.edit_text("Нажаль користувач не погодився із правилами. Доступ до групи заборонено.")
            await bot.kick_chat_member(chat_id=call.message.chat.id, user_id=user_id)
