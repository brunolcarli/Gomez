'''
Módulo para configurações
'''
from decouple import config
from expiringdict import ExpiringDict


MESSAGE_SPAM_FILTER = ExpiringDict(max_len=500, max_age_seconds=30)

TOKEN = config('TOKEN')
LISA_URL = config('LISA')

msg_flood = 5
msg_interval = 20
