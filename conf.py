import os

import telebot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)