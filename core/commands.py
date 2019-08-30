from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json
import ast
from random import choice, randint
from core.settings import TOKEN, MESSAGE_SPAM_FILTER

from util.nlp import (get_offense_level, basic_preprocess, binary_wordmatch,
                    text_classifier, get_random_blablabla, get_the_right_answer)
from util.output_vectors import offended, insufficiency_recognition, opinions



lawton_is_blocked = False

def answer_chat(bot, update):
    """
    Answers a mention message
    """
    chat_id = update.message.chat_id
    text = update.message.text

    is_offensive, _ = get_offense_level(
        basic_preprocess(text)
    )

    # Se for uma mensagem ofensiva
    if is_offensive:
        bot.send_message(chat_id=chat_id, text=choice(offended))

    else:
        # Mensagens de saudações
        greeting_msgs = [
            'oi', 'olá', 'saudações', 'namastê', 'bom dia', 'boa tarde',
        ]

        # Mensagens de despedida
        byebye_msgs = [
            'tchau', 'até logo', 'até mais', 'até breve', 'adeus', 'bye'
        ]

        chat_message = basic_preprocess(text)
        sender = update['message'].to_dict().get('from')
        first_name = sender.get('first_name')
        last_name = sender.get('last_name')
        name = '{} {}'.format(first_name, last_name)

        # Se a mensagem enviada for um cumprimento
        if binary_wordmatch(chat_message, greeting_msgs):
            bot.send_message(
                chat_id=chat_id,
                text=f"{choice(greeting_msgs).capitalize()} {name}!"
            )

        # se for uma mensagem de despedida
        elif binary_wordmatch(chat_message, byebye_msgs):
            bot.send_message(
                chat_id=chat_id,
                text=f"{choice(byebye_msgs).capitalize()} {name}!"
            )

    if '@GomezAddamsBot' in text:
        _, message = text.split('@GomezAddamsBot')

        # Verifica se é uma pergunta
        if '?' in message:
            text_emotion = text_classifier(message)

            if text_emotion < 0:
                response = '{}{}'.format(
                    choice(insufficiency_recognition[0]),
                    choice(insufficiency_recognition[1])
                )
            else:
                # Probabilidade de enrolação
                fill_the_sausage = randint(0, 10)
                if fill_the_sausage > 6:
                    response = get_random_blablabla()
                else:
                    response = '{}{}'.format(
                        choice(opinions[0]),
                        choice(opinions[1])
                    )
            bot.send_message(chat_id=chat_id, text=response)
        else:
            response = get_the_right_answer(message)

            bot.send_message(chat_id=chat_id, text=response)


def roll(bot, update):
    """
    Rolls a six side dice
    """
    chat_id = update.message.chat_id
    sender = update['message'].to_dict().get('from')
    first_name = sender.get('first_name')
    last_name = sender.get('last_name')
    name = '{} {}'.format(first_name, last_name)
    text = '{} rolou {}...'.format(name, str(randint(1, 6)))
    return bot.send_message(chat_id=chat_id, text=text)


def ping(bot, update):
    """
    Pings the bot
    """
    chat_id = update.message.chat_id
    return bot.send_message(chat_id=chat_id, text='pong')


# to send pics
# bot.send_photo(chat_id=chat_id, photo=url

def run():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('ping', ping))
    dp.add_handler(CommandHandler('roll', roll))
    dp.add_handler(MessageHandler(Filters.text, answer_chat))
    updater.start_polling()
    updater.idle()
