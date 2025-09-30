"""Database module for Redis integration."""

import json
import logging
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
        # Serialize nested data to JSON string for Redis hash storage
        serialized_data = {k: json.dumps(v) if isinstance(v, (dict, list)) else str(v) for k, v in data.items()}
        client.hset(key, mapping=serialized_data)
        return True
    except redis.RedisError as e:
        logging.error("Redis error storing user data for user_id=%s: %s", user_id, e)
        return False


def get_user_data(user_id: str) -> Optional[dict]:
    """Retrieve user data from Redis."""
    try:
        client = get_redis_client()
        key = f"user:{user_id}"
        data = client.hgetall(key)
        return data if data else None  # type: ignore
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
        return client.get(key)  # type: ignore
    except redis.RedisError:
        return None
