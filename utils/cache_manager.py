'''
This module defines the cache manager for the APIs.
'''

# External Imports
import json
import redis.asyncio as redis
from redis.exceptions import ConnectionError as RedisConnectionError


class CacheManager:
    ''' A class to manage the caching of products. '''
    def __init__(self, expiration=600):
        self.client = redis.Redis(host='localhost', port=6379, db=0)
        self.expiration = expiration

    async def test_connection(self) -> bool:
        ''' Test the connection to Redis. '''
        if self.client is None:
            return False
        try:
            await self.client.ping()  # Ping Redis
            print("Redis is available.")
            return True
        except RedisConnectionError:
            print("Warning: Redis is not available. Caching is disabled.")
            self.client = None
            return False

    async def is_price_changed(self, product) -> bool:
        ''' Check if the price of the product has changed. '''
        if self.client is None:
            print("Skipping cache: Redis is unavailable.")
            return True

        try:
            cached_product = await self.client.get(product["product_title"])
            if cached_product:
                cached_product_data = json.loads(cached_product.decode("utf-8"))
                if cached_product_data["product_price"] == product["product_price"]:
                    return False
            await self.client.setex(product["product_title"], self.expiration, json.dumps(product))
            return True
        except RedisConnectionError as rce:
            print("utils/cache_manager/is_price_changed/RedisConnectionError: ", rce)
            return True
        except Exception as e:
            print("utils/cache_manager/is_price_changed/Exception: ", e)
            return True
