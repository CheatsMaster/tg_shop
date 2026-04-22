from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Используем относительные импорты
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.supabase_client import SupabaseService
from services.calculation_service import CalculationService
from keyboards.user import get_servers_keyboard, get_cancel_keyboard
from config import Config

router = Router()

class SellForm(StatesGroup):
    choosing_project = State()
    choosing_server = State()
    entering_amount = State()
    confirm = State()

@router.callback_query(F.data == "sell_to_shop")
async def start_sell(callback: types.CallbackQuery, state: FSMContext):
    projects = await SupabaseService.get_projects()
    if not projects:
        await callback.message.edit_text("😔 Нет активных проектов для продажи.")
        return
    
    keyboard = get_servers_keyboard(projects, "sell_project")
    await callback.message.edit_text(
        "💰 <b>Продажа валюты магазину</b>\n\n"
        "Выберите проект:",
        reply_markup=keyboard
    )
    await state.set_state(SellForm.choosing_project)

@router.callback_query(F.data.startswith("sell_project_"))
async def process_project(callback: types.CallbackQuery, state: FSMContext):
    project_id = callback.data.split("_")[2]
    servers = await SupabaseService.get_servers_by_project(project_id)
    
    await state.update_data(project_id=project_id)
    keyboard = get_servers_keyboard(servers, "sell_server", is_server=True)
    
    await callback.message.edit_text(
        "Выберите сервер:",
        reply_markup=keyboard
    )
    await state.set_state(SellForm.choosing_server)

@router.callback_query(F.data.startswith("sell_server_"))
async def process_server(callback: types.CallbackQuery, state: FSMContext):
    server_id = callback.data.split("_")[2]
    server_info = await SupabaseService.get_server_with_price(server_id)
    
    await state.update_data(
        server_id=server_id,
        buy_price=server_info["buy_price"],
        server_name=server_info["name"],
        project_name=server_info["project_name"]
    )
    
    await callback.message.edit_text(
        f"📊 <b>{server_info['project_name']} - {server_info['name']}</b>\n"
        f"💵 Курс покупки: <b>{server_info['buy_price']} ₽</b> за 1 единицу\n\n"
        f"Введите сумму валюты, которую хотите продать:",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(SellForm.entering_amount)

@router.message(SellForm.entering_amount)
async def process_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
    except ValueError:
        await message.answer("❌ Пожалуйста, введите корректное число")
        return
    
    data = await state.get_data()
    total = CalculationService.calculate_total(amount, data["buy_price"])
    
    await state.update_data(amount=amount, total=total)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="sell_confirm")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="sell_cancel")]
    ])
    
    await message.answer(
        f"📋 <b>Проверьте данные:</b>\n\n"
        f"🎮 Проект: {data['project_name']}\n"
        f"🖥 Сервер: {data['server_name']}\n"
        f"💰 Сумма: {amount}\n"
        f"💵 Курс: {data['buy_price']} ₽\n"
        f"📊 <b>Итого к получению: {total} ₽</b>\n\n"
        f"Подтверждаете продажу?",
        reply_markup=keyboard
    )
    await state.set_state(SellForm.confirm)

@router.callback_query(F.data == "sell_confirm")
async def confirm_sell(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = await SupabaseService.get_user(callback.from_user.id)
    
    if not user:
        await callback.message.edit_text("❌ Ошибка: пользователь не найден")
        return
    
    # Создаем заявку
    transaction = await SupabaseService.create_transaction(
        user_id=user["id"],
        server_id=data["server_id"],
        type="sell",
        amount=data["amount"],
        price_per_unit=data["buy_price"],
        total=data["total"]
    )
    
    # Отправляем уведомление админам
    for admin_id in Config.ADMIN_IDS:
        try:
            await callback.bot.send_message(
                admin_id,
                f"🔔 <b>Новая заявка на продажу!</b>\n\n"
                f"👤 Пользователь: @{user.get('username') or user.get('first_name', 'Unknown')}\n"
                f"🎮 {data['project_name']} - {data['server_name']}\n"
                f"💰 Сумма: {data['amount']}\n"
                f"💵 Итого: {data['total']} ₽\n\n"
                f"Свяжитесь с пользователем для завершения сделки."
            )
        except:
            pass
    
    await callback.message.edit_text(
        "✅ <b>Заявка успешно создана!</b>\n\n"
        "Администратор скоро свяжется с вами для завершения сделки.\n"
        "Спасибо, что выбрали Crash Shop! 🛍"
    )
    await state.clear()

@router.callback_query(F.data == "sell_cancel")
async def cancel_sell(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Операция отменена")

@router.callback_query(F.data == "cancel")
async def cancel_any(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    from handlers.user.start import cmd_start
    await cmd_start(callback.message)