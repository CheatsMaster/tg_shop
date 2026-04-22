from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from bot.services.supabase_client import SupabaseService
from bot.config import Config

class RoleMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        
        # Админам доступно всё
        if user_id in Config.ADMIN_IDS:
            return await handler(event, data)
        
        # Проверяем админские команды
        if isinstance(event, Message) and event.text:
            if event.text.startswith('/admin') or event.text.startswith('/broadcast'):
                await event.answer("⛔ У вас нет доступа к этой команде.")
                return
        
        # Проверяем админские callback'и
        if isinstance(event, CallbackQuery):
            if event.data and event.data.startswith('admin_'):
                await event.answer("⛔ Доступ запрещен.", show_alert=True)
                return
        
        return await handler(event, data)