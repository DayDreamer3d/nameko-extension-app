""" Contains request cache related functions
"""
import hashlib


cache_key_delimiter = ':'


def get_hash(master_key, item):
    """ Get hash for the item
    """
    item_key = (master_key + cache_key_delimiter + item.name)
    item_hash = hashlib.md5(item_key.encode()).hexdigest().encode()
    return item_hash


def person_exists(redis_server, master_key, item):
    """ Check if a person exists in cache
    """
    return redis_server.exists(get_hash(master_key, item))


def add_people(redis_server, master_key, items):
    """ Add people to cache
    """
    for item in items:
        item_hash = get_hash(master_key, item)

        # add item info. as hash
        redis_server.hset(item_hash, item.name.encode(), item.age)

        # add item key in sorted set
        redis_server.zadd(master_key, redis_server.zcard(master_key), item_hash)


def get_people(redis_server, master_key):
    """ Get people from cache
    """
    items = {}
    for item_hash in redis_server.zrange(master_key, 0, -1):
        item_info = redis_server.hgetall(item_hash)
        if item_info:
            for name, age in item_info.items(): 
                items[name] = int(age)
    return items
