import asyncio
from app.bot import dp
from app.webserver import run_webserver
from app.handlers import new_members, commands

# Реєструємо обробники
new_members.register_handlers(dp)
commands.register(dp)

async def main():
    # Запускаємо webserver і polling паралельно
    await dp.bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(
        run_webserver(),
        dp.start_polling()
    )

if __name__ == "__main__":
    asyncio.run(main())