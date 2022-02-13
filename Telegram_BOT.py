import json

import requests
import telebot


TOKEN = "5180656271:AAEqHmDgVzGDSyd6DujBVELqB6h-DaBcyY8"

bot = telebot.TeleBot(TOKEN)
# используем API сайта https://www.currate.ru
# https://currate.ru/api/?get=rates&pairs=USDRUB,EURRUB&key=10e8880027ea415e69b7711a2525078
key_API = '10e8880027ea415e69b7711a2525078c'

values = {
    'рубль': 'RUB',
    'доллар': 'USD',
    'евро': 'EUR',
}


class APIException(Exception):
    pass

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

    # Обрабатываем исключения
    if len(vals) != 3:
        raise APIException(f'Неверный запрос. Вводить запрос в одну строку через пробел - 3 параметра')
    qt, bs, amnt = vals

    try:
        amnt = float(amnt)
    except ValueError:
        raise APIException(f'Не удалось обработать {amnt}. Количество ввалют должно быть введенно цифрой')

    try:
        qt_ = values[qt]
    except KeyError:
        raise APIException(f'Не удалось обработать валюту {qt_}.')

    try:
        bs_ = values[bs]
    except KeyError:
        raise APIException(f'Не удалось обработать валюту {bs_}.')

    if qt == bs:
        raise APIException(f'Валюта {qt} не может быть переведена в валюту {bs} - одинаковые!')


    r = requests.get(f'https://currate.ru/api/?get=rates&pairs={values[qt]}{values[bs]}&key={key_API}')
    # content = {'status': 200, 'message': 'rates', 'data': {'USDRUB': '64.1824'}}
    txt_API_json = json.loads(r.content)['data'][f'{values[qt]}{values[bs]}']
    text = f'Цена {amnt} {qt} в {bs} - {txt_API_json}'
    bot.send_message(message.chat.id, text)


bot.polling(non_stop=True)
