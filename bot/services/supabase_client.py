import os
from supabase import create_client, Client
from bot.config import Config

class SupabaseService:
    _client: Client = None
    
    @classmethod
    def get_client(cls) -> Client:
        """Получить клиент Supabase (синглтон)"""
        if cls._client is None:
            cls._client = create_client(
                Config.SUPABASE_URL,
                Config.SUPABASE_KEY
            )
        return cls._client
    
    @staticmethod
    async def get_or_create_user(telegram_id: int, username: str, first_name: str, last_name: str):
        """Получить или создать пользователя"""
        client = SupabaseService.get_client()
        
        # Проверяем существует ли пользователь
        response = client.table('users').select('*').eq('telegram_id', telegram_id).execute()
        
        if response.data:
            return response.data[0]
        
        # Создаем нового пользователя
        new_user = {
            'telegram_id': telegram_id,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'role': 'admin' if telegram_id in Config.ADMIN_IDS else 'user'
        }
        
        response = client.table('users').insert(new_user).execute()
        return response.data[0] if response.data else new_user
    
    @staticmethod
    async def get_user(telegram_id: int):
        """Получить пользователя по telegram_id"""
        client = SupabaseService.get_client()
        response = client.table('users').select('*').eq('telegram_id', telegram_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    async def get_projects():
        """Получить все активные проекты"""
        client = SupabaseService.get_client()
        response = client.table('projects').select('*').eq('is_active', True).execute()
        return response.data
    
    @staticmethod
    async def get_servers_by_project(project_id: str):
        """Получить серверы проекта"""
        client = SupabaseService.get_client()
        response = client.table('servers').select('*').eq('project_id', project_id).eq('is_active', True).execute()
        return response.data
    
    @staticmethod
    async def get_server_with_price(server_id: str):
        """Получить сервер с ценой"""
        client = SupabaseService.get_client()
        
        # Получаем сервер
        server_response = client.table('servers').select('*, projects(name)').eq('id', server_id).execute()
        if not server_response.data:
            return None
        
        server = server_response.data[0]
        
        # Получаем цену
        price_response = client.table('prices').select('*').eq('server_id', server_id).eq('is_active', True).execute()
        
        result = {
            'name': server['name'],
            'project_name': server['projects']['name'] if server.get('projects') else 'Unknown',
            'buy_price': price_response.data[0]['buy_price'] if price_response.data else 0,
            'sell_price': price_response.data[0]['sell_price'] if price_response.data else 0
        }
        
        return result
    
    @staticmethod
    async def create_transaction(user_id: str, server_id: str, type: str, amount: float, price_per_unit: float, total: float):
        """Создать транзакцию"""
        client = SupabaseService.get_client()
        
        transaction = {
            'user_id': user_id,
            'server_id': server_id,
            'type': type,
            'amount': amount,
            'price_per_unit': price_per_unit,
            'total': total,
            'status': 'pending'
        }
        
        response = client.table('transactions').insert(transaction).execute()
        return response.data[0] if response.data else transaction