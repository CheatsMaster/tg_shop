from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from supabase import create_client, Client

app = Flask(__name__)
CORS(app)

# Supabase клиент
supabase: Client = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

@app.route('/api/prices', methods=['GET'])
def get_prices():
    """Получение всех цен с информацией о серверах и проектах"""
    response = supabase.table('prices')\
        .select('*, servers(*, projects(*))')\
        .eq('is_active', True)\
        .execute()
    
    return jsonify(response.data)

@app.route('/api/servers', methods=['GET'])
def get_servers():
    """Получение списка серверов"""
    response = supabase.table('servers')\
        .select('*, projects(*)')\
        .eq('is_active', True)\
        .execute()
    
    return jsonify(response.data)

@app.route('/api/admin/prices', methods=['PUT'])
def update_price():
    """Обновление цены (только для админов)"""
    data = request.json
    telegram_id = request.headers.get('X-Telegram-User-Id')
    
    # Проверка прав администратора
    user = supabase.table('users')\
        .select('role')\
        .eq('telegram_id', telegram_id)\
        .single()\
        .execute()
    
    if not user.data or user.data['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    response = supabase.table('prices')\
        .update({
            'buy_price': data['buy_price'],
            'sell_price': data['sell_price'],
            'discount_percent': data.get('discount_percent', 0)
        })\
        .eq('id', data['id'])\
        .execute()
    
    return jsonify(response.data)

@app.route('/api/admin/broadcast', methods=['POST'])
def broadcast_message():
    """Рассылка сообщения всем пользователям"""
    data = request.json
    telegram_id = request.headers.get('X-Telegram-User-Id')
    
    # Проверка прав
    user = supabase.table('users')\
        .select('role')\
        .eq('telegram_id', telegram_id)\
        .single()\
        .execute()
    
    if not user.data or user.data['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Получаем всех пользователей
    users = supabase.table('users').select('telegram_id').execute()
    
    # Отправляем сообщение через бота (нужен вебхук)
    # Здесь можно использовать aiogram бота через вебхук
    
    return jsonify({'success': True, 'count': len(users.data)})

# Webhook для Telegram бота
@app.route('/api/webhook', methods=['POST'])
def webhook():
    """Обработка вебхуков от Telegram"""
    # Здесь будет обработка обновлений от Telegram
    # для работы бота на Vercel
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)