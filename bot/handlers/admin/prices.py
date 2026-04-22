from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class PriceForm(StatesGroup):
    choosing_server = State()
    entering_price = State()

@router.callback_query(F.data == "admin_panel")
async def admin_panel(callback: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="💰 Управление ценами", callback_data="admin_prices")],
        [types.InlineKeyboardButton(text="📦 Инвентарь", callback_data="admin_inventory")],
        [types.InlineKeyboardButton(text="🖥 Серверы", callback_data="admin_servers")],
        [types.InlineKeyboardButton(text="📢 Рассылка", callback_data="admin_broadcast")],
        [types.InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
    ])
    
    await callback.message.edit_text(
        "⚙️ <b>Админ-панель Crash Shop</b>\n\nВыберите раздел:",
        reply_markup=keyboard
    )

@router.callback_query(F.data == "admin_prices")
async def admin_prices(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "💰 <b>Управление ценами</b>\n\nФункция в разработке.",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="◀️ Назад", callback_data="admin_panel")]
        ])
    )