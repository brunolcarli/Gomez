from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json
import ast
from random import choice, randint
from core.settings import TOKEN, LISA_URL, MESSAGE_SPAM_FILTER


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


data = []
xinga=["paquita do capeta!", "espantalho do fandangos", "bife de rato", "saco de vacilo", "saco de lixo de peruca", "geladinho de chorume", "bafo de bunda", "metralhadora de bosta", "sofá de zona", "filhote de lombriga", "cara de cu com cãibra", "vai coçar o cu com serrote", "enfia um rojão no cu e sai voando", "você não vale o peido de uma jumenta", "você nasceu pelo cu", "vai chupar um prego até virar tachinha", "vai arrastar o cu na brita", "você come pizza com colher", "arrombado do caralho", "chifrudo", "sua mãe tem pelo no dente", "o padre te benzeu com agua parada", "seu monte de esterco", "seu pai vende carta de magic roubada pra ver site porno na lan house"]
def logger(bot, update):
    #bot.send_message(chat_id=update.message.chat_id, text=msg)
    msg=str(update.message.chat_id)+":"+str(update.message.from_user.id)+":"+str(update.message.message_id)
    print ("[!][logger] " + msg)
    data.append(msg)
    Timer(msg_interval, noflood, [bot, update]).start()

def deleteMsgs(bot, update, msgIDs):
    chat_id=str(update.message.chat_id)
    user_id=str(update.message.from_user.id)
    for msg in msgIDs[msg_flood:]:
        Thread(target=deleteMsg, args=(bot, update, int(msg),),).start()
    msg="[!] Cala a boca " + str(update.message.from_user.first_name) + ", " + str(random.choice(xinga)) + "!"
    bot.send_message(chat_id,msg)

def deleteMsg(bot, update, msgId):
    chat_id=update.message.chat_id
    print ("[!][deleteMsg] Deleting => " + str(msgId))
    bot.delete_message(chat_id=chat_id, message_id=msgId)

def noflood(bot, update):
    chat_id=str(update.message.chat_id)
    user_id=str(update.message.from_user.id)
    counter = 0
    msgIds = []
    for i, item in enumerate(data):
#        print(chat_id+":"+user_id)
        print(item)
        if (chat_id + ":" + user_id) in item:
            msgIds.append((data[i].split(":")[2]))
            counter += 1
    if counter >= msg_flood:
#        msg="[!] Cala a boca " + str(update.message.from_user.first_name) + ", " + str(xinga[randint(0, 23)]) + "!"
#        bot.send_message(chat_id,msg)
        data.clear()
#        for msg in msgIds[msg_flood:]:
#            Thread(target=deleteMsg, args=(bot, update, int(msg),),).start()
        deleteMsgs(bot, update,msgIds)
    elif counter < msg_flood:
        data.clear()

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

def run():
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
        Filters.animation | Filters.photo | Filters.video, logger
    ))
    dp.add_handler(MessageHandler(Filters.text, learn))
    
    # dp.add_handler(MessageHandler(Filters.all, spam_clean))
    updater.start_polling()
    updater.idle()
