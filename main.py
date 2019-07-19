from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import re
import json
from random import choice, randint
import redis
import ast
from settings import TOKEN, LISA_URL
from keep_alive import keep_alive

MESSAGE_SPAM_FILTER = redis.Redis(db=10)


lawton_is_blocked = False

def answer_mention(bot, update):
    '''
        Answers a mention message
    '''
    chat_id = update.message.chat_id
    text = update.message.text

    if '@GomezAddamsBot' in text:
        _, message = text.split('@GomezAddamsBot')

        # Solicita resposta de wernicke  à Lisa
        part_1 = "{\"query\":\"mutation{\\n  askGomez(input:{\\n    question: \\\""
        part_2 = "\\\"\\n  }){\\n    response\\n  }\\n}\"}"
        mutation = part_1 + message + part_2
        headers = {
            'content-type': "application/json"
        }

        response = requests.request("POST", LISA_URL, data=mutation, headers=headers)
        response = json.loads(response.text)

        try:
            wernicke_response = response['data']['askGomez'].get('response')
        except:
            wernicke_response = 'Desculpe a Lisa está dodói...'


        bot.send_message(chat_id=chat_id, text=wernicke_response)


def learn(bot, update):
    '''
        Learn all sent messages in the chat.
    '''
    chat_id = update.message.chat_id
    message = update.message.text

    # Alimenta o banco da API
    part_1 = "{\"query\":\"mutation{\\n  askGomez(input:{\\n    question: \\\""
    part_2 = "\\\"\\n  }){\\n    response\\n  }\\n}\"}"
    mutation = part_1 + message + part_2
    headers = {
        'content-type': "application/json"
    }

    response = requests.request("POST", LISA_URL, data=mutation, headers=headers)
    response = json.loads(response.text)

    try:
        wernicke_response = response['data']['askGomez'].get('response')
    except:
        wernicke_response = ''

    # TODO mover essa validação para outro arquivo
    chat_answer = [
        bool(randint(0, 1)),
        bool(randint(0, 1)),
        bool(randint(0, 1)),
    ]
    if all(chat_answer) and wernicke_response:
        bot.send_message(chat_id=chat_id, text=wernicke_response)

def roll(bot, update):
    '''
        Rolls a six side dice
    '''
    chat_id = update.message.chat_id
    sender = update['message'].to_dict().get('from')
    first_name = sender.get('first_name')
    last_name = sender.get('last_name')
    name = '{} {}'.format(first_name, last_name)
    text = '{} rolou {}...'.format(name, str(randint(1, 6)))
    return bot.send_message(chat_id=chat_id, text=text)

def block_lawton(bot, update):
    chat_id = update.message.chat_id
    global lawton_is_blocked
    lawton_is_blocked = True
    text = 'Lawters agora está porobido de mandar fotos.'
    return bot.send_message(chat_id=chat_id, text=text)

def unblock_lawton(bot, update):
    chat_id = update.message.chat_id
    global lawton_is_blocked
    lawton_is_blocked = False
    text = 'Lawters agora está liberado para mandar fotos.'
    return bot.send_message(chat_id=chat_id, text=text)

def spam_clean(bot, update):
    chat_id = update.message.chat_id
    sender = update['message'].to_dict().get('from')
    first_name = sender.get('first_name')
    last_name = sender.get('last_name')
    name = '{} {}'.format(first_name, last_name)

    user_id = sender.get('id')
    message_id = update['message']['message_id']

    if 'lawton' in name.lower() and lawton_is_blocked:
        bot.delete_message(
            chat_id=chat_id,
            message_id=message_id,
        )
    else:
        if str(user_id).encode('utf-8') in MESSAGE_SPAM_FILTER.keys():
            user_data = ast.literal_eval(
                MESSAGE_SPAM_FILTER.get(user_id).decode('utf-8')
            )
            user_data['messages'].append(message_id)
            MESSAGE_SPAM_FILTER.set(
                user_id,
                str(user_data),
                ex=60
            )

            # verifica o número de mensagens enviadas pelo usuário nos últimos 30s
            num_messages = len(user_data['messages'])

            if num_messages > 5 and num_messages < 10:
                text = 'Você está mandando muitas mensagens {}.'.format(
                    name
                )
                return bot.send_message(chat_id=chat_id, text=text)

            elif num_messages >= 10:
                text='Você mandou mensagens demais {}, estou apagando-as.'.format(
                    name
                )
                bot.send_message(chat_id=chat_id, text=text)
                for message in user_data['messages']:
                    bot.delete_message(
                        chat_id=chat_id,
                        message_id=message,
                    )
                MESSAGE_SPAM_FILTER.delete(user_id)
            
        else:
            user_data = {
                'name': name,
                'messages': [message_id]
            }
            MESSAGE_SPAM_FILTER.set(
                user_id,
                str(user_data),
                ex=300
            )

def ping(bot, update):
    '''
        Pings the bot
    '''
    chat_id = update.message.chat_id
    return bot.send_message(chat_id=chat_id, text='pong')

def quote(bot, update):
    '''
        Saves a message to be forever remebered.
    '''
    chat_id = update.message.chat_id

    try:
        _, text = update['message']['text'].split('/quote ')
    except ValueError:
        text = 'Você precisa inserir uma pérola.'
        return bot.send_message(chat_id=chat_id, text=text)

    else:
        part_1 = "{\"query\":\"mutation{\\n  createGomezQuote(input:{\\n    quote: \\\" " 
        part_2 = "\\\"\\n  }){\\n    response\\n  }\\n}\"}"
        headers = {
            'content-type': "application/json"
        }
        payload = part_1 + text.encode('utf-8').hex()  + part_2

        response = requests.request("POST", LISA_URL, data=payload, headers=headers)
        response = json.loads(response.text)

        response = response['data']['createGomezQuote'].get('response')
        response = bytes.fromhex(response).decode('utf-8')

        return bot.send_message(chat_id=chat_id, text=response)

def random_quote(bot, update):
    '''
        Returns a random quote saved in the database
    '''
    chat_id = update.message.chat_id

    payload = "{\"query\":\"query{\\n  gomezQuotes\\n}\"}"
    headers = {
        'content-type': "application/json"
    }

    response = requests.request("POST", LISA_URL, data=payload, headers=headers)
    response = json.loads(response.text)

    quotes = response['data'].get('gomezQuotes')
    if quotes:
        chosen_quote = choice(quotes)
        response = bytes.fromhex(chosen_quote).decode('utf-8')
    else:
        response = 'Desculpe mas minha memória não está muito boa agora...'

    return bot.send_message(chat_id=chat_id, text=response)

def frase_do_lawton(bot, update):
    '''
        Returns a Lwaton classic.
    '''
    chat_id = update.message.chat_id
    lawters = [
        'Tendeu né?', 'Nhííííííííííí', 'Flip Flop', 'Prestenção',
        'Você não sabe o que é frio!'
        ]
    return bot.send_message(chat_id=chat_id, text=choice(lawters))

# to send pics
# bot.send_photo(chat_id=chat_id, photo=url

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('ping', ping))
    dp.add_handler(CommandHandler('quote', quote))
    dp.add_handler(CommandHandler('roll', roll))
    dp.add_handler(CommandHandler('random_quote', random_quote))
    dp.add_handler(CommandHandler('block_lawton', block_lawton))
    dp.add_handler(CommandHandler('unblock_lawton', unblock_lawton))
    dp.add_handler(CommandHandler('frase_do_lawton', frase_do_lawton))
    dp.add_handler(MessageHandler(Filters.text, answer_mention))
    dp.add_handler(MessageHandler(
        Filters.video | Filters.photo | Filters.document | Filters.sticker, spam_clean)
    )
    dp.add_handler(MessageHandler(Filters.text, learn))
    
    # dp.add_handler(MessageHandler(Filters.all, spam_clean))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    keep_alive()
    print('Running')
    main()
