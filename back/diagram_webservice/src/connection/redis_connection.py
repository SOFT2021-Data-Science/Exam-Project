import redis

def make_redis_pool():
    """Creates and returns redis connection pool

    :return: Redis connection pool
    :rtype: redis.Redis()
    """    
    return redis.Redis(host="localhost", port=6379, db=0)
