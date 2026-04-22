from aiogram import Router, types, F
from bot.services.supabase_client import SupabaseService

router = Router()

@router.callback_query(F.data == "view_prices")
async def view_prices(callback: types.CallbackQuery):
    projects = await SupabaseService.get_projects()
    
    if not projects:
        await callback.message.edit_text("😔 Нет активных проектов.")
        return
    
    text = "💰 <b>Текущие курсы валют:</b>\n\n"
    
    for project in projects:
        text += f"🎮 <b>{project['name']}</b>\n"
        servers = await SupabaseService.get_servers_by_project(project['id'])
        
        for server in servers:
            price_info = await SupabaseService.get_server_with_price(server['id'])
            text += f"  • {server['name']}\n"
            text += f"    Покупка: {price_info['buy_price']}₽ | Продажа: {price_info['sell_price']}₽\n"
        
        text += "\n"
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🔄 Обновить", callback_data="view_prices")],
        [types.InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    from bot.handlers.user.start import cmd_start
    await cmd_start(callback.message)