CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://cache:6379",
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'db',
        'PORT': '5432',
        'USER': 'app',
        'PASSWORD': 'app',
        'NAME': 'app',
        'OPTIONS': {
            'client_encoding': 'UTF8',
            'connect_timeout': 3600,
        }
    }
}
