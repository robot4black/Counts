import os
import requests

TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')

url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage'

def send_file_content(filename):
    with open(filename, 'r') as f:
        content = f.read()
    data = {
        'chat_id': TG_CHAT_ID,
        'text': content
    }
    resp = requests.post(url, data=data)

send_file_content('output_1.txt')
send_file_content('output_3.txt')
