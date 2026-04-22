from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'ok',
        'service': 'Crash Shop API',
        'version': '1.0.0'
    })

@app.route('/api/prices', methods=['GET'])
def get_prices():
    return jsonify({
        'prices': [
            {'project': 'Radmir Online', 'server': 'Radmir #1', 'buy': 100, 'sell': 95},
            {'project': 'Amazing Online', 'server': 'Amazing RP', 'buy': 50, 'sell': 45}
        ]
    })

# Для Vercel serverless functions
def handler(request, response):
    return app(request, response)