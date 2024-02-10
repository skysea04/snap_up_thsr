import os

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        'LOCATION': f'redis://{os.environ.get("REDIS_HOST")}:{os.environ.get("REDIS_PORT", 6379)}?health_check_interval=30',
    },
    'OPTIONS': {
        'SOCKET_TIMEOUT': 30,
        'SOCKET_CONNECT_TIMEOUT': 30,
        'CONNECTION_POOL_CLASS': 'redis.connection.BlockingConnectionPool',
        'CONNECTION_POOL_KWARGS': {
            'max_connections': 1000,
            'timeout': 30,
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'NAME': os.environ.get('DB_NAME'),
        'OPTIONS': {
            'client_encoding': 'UTF8',
            'connect_timeout': 3600,
        }
    }
}
