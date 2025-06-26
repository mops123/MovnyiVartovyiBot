# handlers/commands.py
from aiogram import Dispatcher, types

def register(dp: Dispatcher):
    @dp.message_handler(commands=["start"])
    async def cmd_start(message: types.Message):
        await message.reply("👋 Я — MovnyiVartovyiBot!")

    @dp.message_handler(commands=["help"])
    async def cmd_help(message: types.Message):
        await message.reply(
        "🤖 Що я вмію:\n"
        "- Вітати нових учасників\n"
        "- Питати згоду на правило української мови\n"
        "- Забороняти писати без згоди\n"
        "- Видаляти, якщо учасник не згоден\n\n"
        "❗ Я не перевіряю повідомлення після згоди — це завдання модераторів."
    )

    @dp.message_handler(commands=["rule"])
    async def cmd_rule(message: types.Message):
        await message.reply("📜 Спілкування — тільки українською.")
