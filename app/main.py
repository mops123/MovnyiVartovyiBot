import asyncio
from aiogram.utils import executor
from app.bot import dp
from app.webserver import run_webserver
from app.handlers import new_members, commands

# Реєструємо обробники
new_members.register_handlers(dp)
commands.register(dp)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_webserver())
    executor.start_polling(dp, skip_updates=True)
