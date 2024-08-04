import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from app.bot.buttons import start, button
from app.config import settings

app_bot = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start_bot():
    global app_bot
    logger.info("Initializing bot...")
    app_bot = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CallbackQueryHandler(button))
    logger.info("Handlers added. Initializing and starting the bot...")

    # Limpar as atualizações pendentes
    updates = await app_bot.bot.get_updates(offset=-1)
    await app_bot.initialize()
    await app_bot.start()
    if updates:
        logger.info("Ignoring pending updates")
    await app_bot.updater.start_polling()
    logger.info("Bot started and polling for updates.")

async def stop_bot():
    global app_bot
    if app_bot:
        logger.info("Stopping bot...")
        await app_bot.updater.stop()
        await app_bot.stop()
        await app_bot.shutdown()
        app_bot = None
        logger.info("Bot stopped.")