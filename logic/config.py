import json

with open('settings.json', 'r', encoding='utf-8-sig') as f:
    bot_settings = json.load(f)['BotSettings']

API_TOKEN = bot_settings.get('token', '')
ADMIN_ID = bot_settings.get('admin_id', '')
TG_LINK = bot_settings.get('link', '')