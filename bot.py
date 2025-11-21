import os
import random
import datetime
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
    """Читаем предсказания из wishes.txt"""
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
            await context.bot.send_message(chat_id, f"✨ Твоё предсказание на сегодня:\n\n{wish}")
        except Exception:
            pass


async def main():
    if not TOKEN:
        raise RuntimeError("❌ BOT_TOKEN НЕ УСТАНОВЛЕН!")

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("stop", stop_command))

    # Ежедневная рассылка в 10:00 по Киеву
    application.job_queue.run_daily(
        send_daily_predictions,
        time=datetime.time(hour=10, minute=0, tzinfo=datetime.timezone(datetime.timedelta(hours=2)))
    )

    print("🚀 Bot is running...")
    await application.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
