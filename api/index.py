from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Добавляем корневую папку в путь для импортов
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'Crash Shop API'})

@app.route('/api/prices', methods=['GET'])
def get_prices():
    # Заглушка, потом подключим Supabase
    return jsonify({
        'prices': [
            {
                'project': 'Radmir Online',
                'server': 'Radmir #1',
                'buy_price': 100,
                'sell_price': 95
            },
            {
                'project': 'Amazing Online',
                'server': 'Amazing RP',
                'buy_price': 50,
                'sell_price': 45
            }
        ]
    })

# Для локального запуска
if __name__ == '__main__':
    app.run(debug=True, port=5000)