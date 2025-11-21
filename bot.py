import os
import asyncio
import random
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

# Загружаем предсказания
def load_wishes():
    try:
        with open("wishes.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return ["Сегодня будет удачный день!"]

WISHES = load_wishes()


# /start — подписаться
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ты подписан на предсказания! Отправь /wish чтобы получить предсказание.")


# /wish — выдать случайное предсказание
async def wish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(WISHES))


async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Регистрируем команды
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("wish", wish))

    # Запуск бота
    await application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
