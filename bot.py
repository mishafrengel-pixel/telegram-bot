import asyncio
from aiogram import Bot, Dispatcher, types

TOKEN = "ТОКЕН_ТВОЕГО_БОТА"

bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message()
async def send_random_wish(message: types.Message):
    with open("wishes.txt", "r", encoding="utf-8") as f:
        wishes = [w.strip() for w in f.readlines() if w.strip()]
    import random
    wish = random.choice(wishes)
    await message.answer(wish)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
