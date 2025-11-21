import os
import random
import datetime

import pytz
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.getenv("8514534127:AAFqPCCu82681KnlektbbA2SJz5z-YunxqI")

# В памяти. После перезапуска сервиса подписи обнулятся — потом можно будет сделать файл/БД.
subscribers: set[int] = set()


def load_wishes() -> list[str]:
    """Читаем предсказания из файла wishes.txt, по одному на строку."""
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
    await update.message.reply_text("Ты отписан от предсказаний.")


async def send_daily_predictions(context: ContextTypes.DEFAULT_TYPE):
    """Эта функция будет вызываться каждый день в 9:00 по Киеву."""
    if not subscribers:
        return

    wishes = load_wishes()
    text = random.choice(wishes)
    msg = f"🔮 Предсказание на сегодня:\n\n{text}"

    for chat_id in list(subscribers):
        try:
            await context.bot.send_message(chat_id=chat_id, text=msg)
        except Exception:
            # если кого-то нельзя доставить — просто пропускаем
            pass


async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("stop", stop_command))

    # Настраиваем ежедневное отправление в 9:00 по Киеву
    kyiv_tz = pytz.timezone("Europe/Kiev")
    time_9 = datetime.time(hour=9, minute=0, tzinfo=kyiv_tz)
    app.job_queue.run_daily(send_daily_predictions, time=time_9)

    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
