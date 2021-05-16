import redis
import os
from utils.misc import load_variables

load_variables()

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DB = os.getenv('REDIS_DB')


def make_redis_pool():
    """Creates and returns redis connection pool

    :return: Redis connection pool
    :rtype: redis.Redis()
    """    
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
