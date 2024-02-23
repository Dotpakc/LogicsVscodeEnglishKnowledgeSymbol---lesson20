import asyncio
import logging

from decouple import config


from aiogram import Bot, Dispatcher, Router, types,F
from aiogram.filters import CommandStart, Command   


TOKEN = config("TOKEN")

dp = Dispatcher() # объект диспетчера (оброботчик событий)
bot = Bot(TOKEN)

# async - асинхронная функция (позволяет не блокировать выполнение кода)
# await - ожидание выполнения асинхронной функции



@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.answer(f"Hello, {message.from_user.full_name}!")




async def main() -> None:
   
    await dp.start_polling(bot)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    asyncio.run(main())