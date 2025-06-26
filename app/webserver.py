import os
from aiohttp import web

async def handle(request):
    return web.Response(text="✅ I'm alive!")

async def run_webserver():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port=port)
    await site.start()
    print(f"🌐 Web server is running on port {port}")
