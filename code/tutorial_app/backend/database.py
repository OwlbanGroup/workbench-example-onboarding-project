"""Database module for Redis integration."""

import os
from typing import Optional
import redis  # pylint: disable=import-error


def get_redis_client() -> redis.Redis:
    """Get Redis client instance."""
    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", "6379"))
    db = int(os.getenv("REDIS_DB", "0"))
    return redis.Redis(host=host, port=port, db=db, decode_responses=True)


def store_user_data(user_id: str, data: dict) -> bool:
    """Store user data in Redis."""
    try:
        client = get_redis_client()
        key = f"user:{user_id}"
        client.hset(key, mapping=data)
        return True
    except redis.RedisError:
        return False


def get_user_data(user_id: str) -> Optional[dict]:
    """Retrieve user data from Redis."""
    try:
        client = get_redis_client()
        key = f"user:{user_id}"
        data = client.hgetall(key)
        return data if data else None
    except redis.RedisError:
        return None


def store_app_data(key: str, value: str) -> bool:
    """Store application data in Redis."""
    try:
        client = get_redis_client()
        client.set(key, value)
        return True
    except redis.RedisError:
        return False


def get_app_data(key: str) -> Optional[str]:
    """Retrieve application data from Redis."""
    try:
        client = get_redis_client()
        return client.get(key)
    except redis.RedisError:
        return None
