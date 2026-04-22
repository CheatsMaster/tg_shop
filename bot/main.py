import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import Config
from bot.handlers.user import start, view_prices, sell_to_shop
from bot.handlers.admin import prices, inventory, servers, broadcast
from bot.middlewares.role_middleware import RoleMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(
        token=Config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())
    
    # Middleware для проверки ролей
    dp.message.middleware(RoleMiddleware())
    dp.callback_query.middleware(RoleMiddleware())
    
    # Регистрация роутеров
    dp.include_router(start.router)
    dp.include_router(view_prices.router)
    dp.include_router(sell_to_shop.router)
    
    # Админские роутеры
    dp.include_router(prices.router)
    dp.include_router(inventory.router)
    dp.include_router(servers.router)
    dp.include_router(broadcast.router)
    
    logger.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())