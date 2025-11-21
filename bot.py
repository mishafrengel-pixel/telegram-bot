import os
import random
from typing import List, Set

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

subscribers: Set[int] = set()


def load_wishes() -> List[str]:
    """Считываем предсказания из wishes.txt"""
    try:
        with open("wishes.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return ["Сегодня будет удачный день"]


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    subscribers.add(chat_id)
    await update.message.reply_text("Ты подписан на ежедневные предсказания! ✨")


async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    subscribers.discard(chat_id)
    await update.message.reply_text("Ты отписан от предсказаний ❌")


async def send_daily_predictions(context: ContextTypes.DEFAULT_TYPE):
    wishes = load_wishes()
    wish = random.choice(wishes)

    for chat_id in list(subscribers):
        try:
            await context.bot.send_message(chat_id, f"Твое предсказание на сегодня:\n\n{wish}")
        except Exception:
            pass


async def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("stop", stop_command))

    application.job_queue.run_daily(
        send_daily_predictions,
        time=None,  # запускает сразу при разворачивании (Render не держит время точно)
    )

    # run_polling — НО НУЖНО ОТКРЫТЬ ПОРТ, чтобы Render понимал, что сервис “живой”
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.idle()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
