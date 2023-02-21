import telebot
from extensions import CryptoConverter, APIException
from config import TOKEN, keys


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['author'])
def author(message: telebot.types.Message):
    bot.reply_to(message, f'{"*" * 20}\n   >>>> ARSmobi <<<<\n             Курбанов'
                          f'\n                Арслан\n Абубакаргаджиевич\n{"*" * 20}')


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты>  \
<в какую валюту перевести>  \
<количество переводимой валюты> \nУвидеть список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n - '.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values_from_message = list(map(lambda x: x.lower(), message.text.split()))
    try:
        if len(values_from_message) > 3:
            raise APIException('Слишком много параметров.')
        elif len(values_from_message) < 3:
            raise APIException('Не достаточно параметров.')

        quote, base, amount = values_from_message
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Ошибка на сервере.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {round(float(total_base) * float(amount), 2)}'
        bot.send_message(message.chat.id, text)


bot.polling()
