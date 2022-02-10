import telebot


TOKEN = "5180656271:AAEqHmDgVzGDSyd6DujBVELqB6h-DaBcyY8"

bot = telebot.TeleBot(TOKEN)

values = {
    'Рубль': 'RUB',
    'Доллар': 'USD',
    'Евро': 'EUR',
}

# Обрабатывает все сообщения, содержащие команды '/start' or '/help'
@bot.message_handler(commands=['help', 'start', ])
def handel_help_start(message: telebot.types.Message):
    bot.reply_to(message, f'Привет, {message.chat.username}!\n Это БОТ для перевода одной валюты в другую. '\
                          '\n Чтобы узнать стоимость валюты нужно отправить сообщение боту в виде '\
                          '\n <имя валюты, цену которой он хочет узнать>'\
                          '\n <имя валюты, в которой надо узнать цену первой валюты>'\
                          '\n <количество первой валюты>')

# Показываем список валют с которыми работает БОТ
@bot.message_handler(commands=['values', ])
def hendel_values(message: telebot.types.Message):
    text = f'Бот работает со следующими валютами:'
    for val in values:
        text = text + f'\nВалюта {val}.'
    bot.reply_to(message, text)


bot.polling(non_stop=True)
