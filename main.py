from core.keep_alive import keep_alive
import redis
from core.commands import run

MESSAGE_SPAM_FILTER = redis.Redis(db=10)


lawton_is_blocked = False


if __name__ == '__main__':
    keep_alive()
    print('Running')
    run()
