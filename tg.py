import os

TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')

from telegram import Bot

def send_file_content(filename):
    with open(filename, 'r') as f:
        content = f.read()

    bot = Bot(token=TG_BOT_TOKEN)
    bot.send_message(chat_id=TG_CHAT_ID, text=content)

if __name__ == "__main__":
    send_file_content('output_1.txt')
    send_file_content('output_3.txt')
