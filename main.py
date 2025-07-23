import telebot
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(message, "Привет! Я твой помощниу по бюджету! $$$")

@bit.message_handler(func=lambda message: True)
def echo_all(message):
  bot.reply_to(message, f"Ты написала: {message.text}")

bot.infinity_polling()
