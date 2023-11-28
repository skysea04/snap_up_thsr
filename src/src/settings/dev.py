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
        'NAME': 'app',
        'USER': 'app',
        'PASSWORD': 'app',
        'PORT': '5432',
        'OPTIONS': {
            'client_encoding': 'UTF8',
            'connect_timeout': 3600,
        }
    }
}

ALLOWED_HOSTS = ['*']
