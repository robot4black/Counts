import os
import requests

TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')


def send_file_content(filename):
    with open(filename, 'r') as f:
        content = f.read()
    data = {
        'chat_id': chat_id,
        'text': content
    }
    resp = requests.post(url, data=data)

send_file_content('output_1.txt')
send_file_content('output_3.txt')
