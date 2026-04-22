from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_servers_keyboard(items: list, callback_prefix: str, is_server: bool = False):
    """Создать клавиатуру с серверами"""
    keyboard = []
    
    for item in items:
        item_id = item.get('id')
        item_name = item.get('name')
        
        keyboard.append([
            InlineKeyboardButton(
                text=f"🎮 {item_name}",
                callback_data=f"{callback_prefix}_{item_id}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_cancel_keyboard():
    """Клавиатура с отменой"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
    ])