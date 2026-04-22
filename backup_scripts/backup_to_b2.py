import os
import json
import b2sdk.v2 as b2
from datetime import datetime
from supabase import create_client

class BackupService:
    def __init__(self):
        self.supabase = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        
        self.b2_api = b2.B2Api()
        self.b2_api.authorize_account(
            "production",
            os.getenv('B2_KEY_ID'),
            os.getenv('B2_APPLICATION_KEY')
        )
        self.bucket = self.b2_api.get_bucket_by_name(os.getenv('B2_BUCKET_NAME'))
    
    async def create_backup(self):
        """Создание полного бэкапа базы данных"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Получаем все данные из таблиц
        tables = ['projects', 'servers', 'prices', 'users', 'inventory', 'transactions']
        backup_data = {}
        
        for table in tables:
            response = self.supabase.table(table).select('*').execute()
            backup_data[table] = response.data
        
        # Сохраняем в JSON
        backup_json = json.dumps(backup_data, default=str, ensure_ascii=False)
        filename = f'backup_{timestamp}.json'
        
        # Загружаем в B2
        self.bucket.upload_bytes(
            backup_json.encode('utf-8'),
            filename,
            content_type='application/json'
        )
        
        print(f'✅ Бэкап создан: {filename}')
        return filename
    
    async def restore_backup(self, filename: str):
        """Восстановление из бэкапа"""
        # Скачиваем из B2
        downloaded_file = self.bucket.download_file_by_name(filename)
        backup_data = json.loads(downloaded_file.download().content)
        
        # Восстанавливаем данные
        for table, data in backup_data.items():
            if data:
                # Очищаем таблицу
                self.supabase.table(table).delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
                # Вставляем данные
                self.supabase.table(table).insert(data).execute()
        
        print(f'✅ Бэкап восстановлен из: {filename}')

# GitHub Actions workflow для автоматических бэкапов
"""
.github/workflows/backup.yml:

name: Daily Backup
on:
  schedule:
    - cron: '0 0 * * *'  # Каждый день в полночь
  workflow_dispatch:

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install supabase b2sdk
      - name: Run backup
        env:
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
          B2_KEY_ID: ${{ secrets.B2_KEY_ID }}
          B2_APPLICATION_KEY: ${{ secrets.B2_APPLICATION_KEY }}
          B2_BUCKET_NAME: ${{ secrets.B2_BUCKET_NAME }}
        run: python backup_scripts/backup_to_b2.py
"""