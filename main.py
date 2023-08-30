from aiogram import Bot, Dispatcher
import asyncio
from routers import all_routers
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token='5548169741:AAEfs60DEdFhEDwwZUHvRSm8fuYu0Ec_qj4', parse_mode='HTML')
dp = Dispatcher(storage=MemoryStorage())

for i in all_routers:
    dp.include_router(i)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    print('Включаюс')
    asyncio.run(main())
