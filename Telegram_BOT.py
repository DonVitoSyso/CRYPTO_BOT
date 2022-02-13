import telebot
from utils import TOKEN, values
from extensions import ValuesConvert, APIException

bot = telebot.TeleBot(TOKEN)

# Обрабатывает все сообщения, содержащие команды '/start' or '/help'
@bot.message_handler(commands=['help', 'start', ])
def handel_help_start(message: telebot.types.Message):
    bot.reply_to(message, f'Привет, {message.chat.username}!\n Это БОТ для перевода одной валюты в другую. '\
                          '\n Чтобы узнать стоимость валюты нужно отправить сообщение боту в виде'\
                          '(вводить в одну строку через пробел) '\
                          '\n <имя валюты, цену которой он хочет узнать>'\
                          '\n <имя валюты, в которой надо узнать цену первой валюты>'\
                          '\n <количество первой валюты>'\
                          '\nУвидеть все доступные валюты можно - /values'
                )

# Показываем список валют с которыми работает БОТ
@bot.message_handler(commands=['values', ])
def hendel_values(message: telebot.types.Message):
    text = 'Бот работает со следующими валютами:'
    for val in values.keys():
        text = '\n'.join((text, val))
    bot.reply_to(message, text)


# Запрос цены валют
@bot.message_handler(content_types=['text', ])
def hendel_convert(message: telebot.types.Message):
    vals = message.text.split(' ')
    base, quote, amount, txt_API_json = ValuesConvert.get_price(vals)
    text = f'Цена {amount} {base} в {quote} - {txt_API_json}'
    bot.send_message(message.chat.id, text)


bot.polling(non_stop=True)
