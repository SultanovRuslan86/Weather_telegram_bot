import telebot
import requests
import json
import sqlite3

bot = telebot.TeleBot('6146979892:AAErxZWGaOiQtVycUSv2NXtJzD0KhgQofmA')
API = '95d51d01275c6d07af3f6a056dbe5bf0'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Назови свой город, а я тебе скажу какая у вас будет погода!')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        key_word = data["weather"][0]["main"]
        speed_of_wind = data["wind"]["speed"]
        bot.reply_to(message, f'Сейчас погода в {city} - {temp} градусов!')
        image = ''
        image_text = ''
        image_text_2 = ''
        if key_word == 'Rain':
            image += 'rain.png'
            image_text += 'Дождь, не забудь взять зонт или дождевик'
            image_text_2 += f'Скорость ветра: {speed_of_wind} m/s'
        elif key_word == 'Clouds':
            image += 'cloud.png'
            image_text += 'Облачно, возможен дождь!'
            image_text_2 += f'Скорость ветра: {speed_of_wind} m/s'
        elif key_word == 'Clear':
            image += 'sun.png'
            image_text += 'Солнечно, не забудь взять солнечные очки и головной убор!'
            image_text_2 += f'Скорость ветра: {speed_of_wind} m/s'
        elif key_word == 'Snow':
            image += 'snow.png'
            image_text += 'Снег, не забудь взять перчатки и одеться потеплее!'
            image_text_2 += f'Скорость ветра: {speed_of_wind} m/s'
        else:
            image += 'cloudy.png'
            image_text += 'Погода просто прелесть!'
            image_text_2 += f'Скорость ветра: {speed_of_wind} m/s'

        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, file)
        bot.send_message(message.chat.id, image_text)
        bot.send_message(message.chat.id, image_text_2)
    else:
        bot.reply_to(message, f'Город указан неверно, проверь название и отправь запрос повторно')

bot.polling(none_stop=True)





