import telebot
from telebot import types
import os
import requests

API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
bot = telebot.TeleBot('6623385674:AAFcfaJPyYUGLPIMd7QMKI67tQOjJRqOEe8')


# Обработчик для команды /start при старте бота
@bot.message_handler(commands=['start'])
def send_currency_buttons(message):
    currency_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    currency_buttons.row("USD", "EUR")
    bot.send_message(message.chat.id, "Привет! Я бот, который поможет вам узнать текущий курс валюты к рублю. "
                                      "Выберите валюту:", reply_markup=currency_buttons)


# Функция для обработки нажатия кнопок с валютами
@bot.message_handler(func=lambda message: message.text in ['USD', 'EUR'])
def handle_currency_button(message):
    currency = message.text

    # Например, отправить сообщение с курсом выбранной валюты
    bot.send_message(message.chat.id, f"Вы выбрали валюту: {currency}. Курс к рублю: {get_currency_rate(currency)}")

# Обработчик для всех сообщений, не являющихся выбором валюты
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_message(message.chat.id, "Непонятная команда. Пожалуйста, используйте кнопки для выбора валюты.")


def get_currency_rate(base: str) -> float:
    """Получает курс валюты от API и возвращает его в виде float"""
    url = "https://api.apilayer.com/exchangerates_data/latest"
    response = requests.get(url, headers={'apikey': API_KEY}, params={'base': base})
    rate = response.json()["rates"]["RUB"]
    return rate

bot.polling()