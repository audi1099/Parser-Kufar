from logging import basicConfig, INFO, error
import os
import random
import re
import time
import requests
import telebot
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openpyxl import Workbook
from openpyxl.styles import Font
from telebot import types

# Константы
CHUNK_LENGTH = 4096  # Максимальная длина сообщения Telegram

# Настройка логирования
basicConfig(level=INFO)

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение токена из переменной окружения
TOKEN = os.getenv("TOKEN")

# Инициализация бота с токеном
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Pixel 7')
    itembtn2 = types.KeyboardButton('Pixel 7A')
    itembtn3 = types.KeyboardButton('Pixel 7 Pro')
    itembtn4 = types.KeyboardButton('Pixel 8')
    itembtn5 = types.KeyboardButton('Pixel 8A')
    itembtn6 = types.KeyboardButton('Pixel 8 Pro')
    itembtn7 = types.KeyboardButton('iPhone 11')
    itembtn8 = types.KeyboardButton('iPhone 12')
    itembtn9 = types.KeyboardButton('iPhone 13')
    itembtn10 = types.KeyboardButton('iPhone 14')
    itembtn11 = types.KeyboardButton('Samsung Galaxy S22')
    itembtn12 = types.KeyboardButton('Другая модель')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8, itembtn9, itembtn10,
               itembtn11, itembtn12)
    bot.reply_to(message, 'Привет! Я бот поиска объявлений на Kufar. Выберите модель телефона или введите другую '
                          'модель:', reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def search(message):
    keyword = message.text
    results = search_products(keyword)
    if not results:
        bot.reply_to(message, "По вашему запросу ничего не найдено.")
        return
    bot.reply_to(message, "Вот результаты поиска:")
    send_results_in_chunks(results, message.chat.id)
    save_to_excel(results, keyword, message)


def search_products(keyword):
    url = f"https://www.kufar.by/l/mobilnye-telefony?query={keyword}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        time.sleep(random.uniform(1, 3))  # Случайная задержка между запросами (от 1 до 3 секунд)
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all('a', class_='styles_wrapper__5FoK7')[:-8]
        results = ""
        for product in products:
            product_data = extract_product_data(product)
            if product_data and keyword.lower() in product_data['name'].lower():
                result = format_product_data(product_data)
                results += result
        return results
    except requests.exceptions.RequestException as e:
        error(f"An error occurred while searching products: {e}")
        return None


def extract_product_data(product):
    product_name = product.find('h3', class_='styles_title__F3uIe')
    product_price = product.find('p', class_='styles_price__G3lbO')
    product_location = product.find('div', class_='styles_secondary__MzdEb')
    product_href = product.get('href')
    if product_href:
        product_href = "https://www.kufar.by" + product_href if product_href.startswith("/") else product_href
    if product_name and product_price and product_location:
        return {
            'name': product_name.text.strip(),
            'price': product_price.text.strip(),
            'location': product_location.text.strip(),
            'href': product_href
        }
    else:
        return None


def format_product_data(product_data):
    return (
        f"Модель: {product_data['name']}\nЦена: {product_data['price']}\nМестоположение: {product_data['location']}\n"
        f"Ссылка на объявление: {product_data['href']}\n\n")


def send_results_in_chunks(results, chat_id):
    chunks = [results[i:i + CHUNK_LENGTH] for i in range(0, len(results), CHUNK_LENGTH)]
    for chunk in chunks:
        try:
            bot.send_message(chat_id, chunk)
        except Exception as e:
            error(f"An error occurred while sending results: {e}")


def save_to_excel(results, keyword, message):
    try:
        wb = Workbook()
        ws = wb.active
        bold_font = Font(bold=True)
        headers = ["Модель", "Цена", "Местоположение", "Ссылка на объявление"]
        ws.append(headers)
        for cell in ws[1]:
            cell.font = bold_font
        rows = results.split("\n\n")
        for row in rows:
            if row:
                data = row.split("\n")
                model = strip_tags(data[0].split(":")[1].strip())
                price = strip_tags(data[1].split(":")[1].strip())
                location = strip_tags(data[2].split(":")[1].strip())
                link = strip_tags(data[3].split(":")[1].strip())
                ws.append([model, price, location, link])
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2) * 1.2
            ws.column_dimensions[column].width = adjusted_width
        filename = f"{keyword}_results.xlsx"
        wb.save(filename)
    except Exception as e:
        error(f"An error occurred while saving to Excel: {e}")
        bot.reply_to(message, "Произошла ошибка при сохранении результатов. Пожалуйста, попробуйте позже.")


def strip_tags(html_text):
    clean_text = re.sub(r'<[^>]+>', '', html_text)
    return clean_text


@bot.message_handler(content_types=['text'])
def handle_errors(message):
    bot.reply_to(message, "Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте позже.")


@bot.message_handler(func=lambda message: True,
                     content_types=['audio', 'document', 'photo', 'sticker', 'video', 'voice', 'location', 'contact',
                                    'new_chat_members', 'left_chat_member', 'new_chat_title', 'new_chat_photo',
                                    'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created',
                                    'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id',
                                    'pinned_message'])
def handle_other(message):
    bot.reply_to(message, "К сожалению, я не могу обработать это.")


bot.polling()

