from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.supabase_client import SupabaseService
from config import Config

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user = await SupabaseService.get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🛒 Открыть Crash Shop",
            web_app=WebAppInfo(url=Config.WEBAPP_URL)
        )],
        [
            InlineKeyboardButton(text="💰 Курсы валют", callback_data="view_prices"),
            InlineKeyboardButton(text="💸 Продать валюту", callback_data="sell_to_shop")
        ]
    ])
    
    if user and user.get("role") == "admin":
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text="⚙️ Админ-панель", callback_data="admin_panel")
        ])
    
    await message.answer(
        f"🎮 Добро пожаловать в <b>Crash Shop</b>!\n\n"
        f"Мы покупаем и продаём виртуальную валюту на проектах:\n"
        f"• Radmir Online\n"
        f"• Amazing Online (CR-MP)\n\n"
        f"Выберите действие:",
        reply_markup=keyboard
    )